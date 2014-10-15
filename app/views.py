import urllib2
import json
from flask import render_template, request, jsonify
from app import app, db, socketio
from models import Song


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", songs=Song.query.all())


@app.route('/api/playlist', methods=['GET', 'POST'])
@app.route('/api/playlist/<start>', methods=['GET', 'POST'])
def playlistAPI(start=False):
    if request.method == 'GET':
        data = getSongs(start)
    if request.method == 'POST':
        data = postSong()
    return jsonify(data)


def getSongs(start=False):
    '''Grabs 50 songs at once, optionally starting at id < "start"'''
    songList = []
    if start:
        query = Song.query.order_by(Song.id.desc()).filter(Song.id < start).limit(50).all()
    else:
        query = Song.query.order_by(Song.id.desc()).limit(50).all()       
    for song in query:
        songDict = {"id": song.id, "url": song.url, "title": song.title}
        songList.append(songDict.copy())
    data = {
        "songList": songList
    }
    return data


def postSong(url=None):
    data = {
        "success": False
    }
    if url is None:
        url = request.json.get('url')
    title = findTitle(url)
    if title is None:
        data["message"] = "Invalid URL!"
        return data
    else:
        if "youtube" in url:
            url = "//www.youtube.com/embed/" + getYoutubeId(url)
        newSong = Song(url=url, title=title)
        db.session.add(newSong)
        try:
            db.session.commit()
        except:
            data["message"] = "Song already in playlist!"
            db.session.rollback()
            return data
        data = {
            "success": True,
            "data": {
                "id": newSong.id,
                "url": newSong.url,
                "title": newSong.title
                }
        }
    socketio.emit('new-song', data['data'])
    return data


def findTitle(url):
    if "soundcloud" in url:
        try:
            response = urllib2.urlopen("http://soundcloud.com/oembed?url=" + cleanSoundcloudUrl(url) + "&format=json")
        except urllib2.HTTPError:
            return None
        soundcloudData = json.load(response)
        return soundcloudData.get('title')
    elif "youtube" in url:
        try:
            response = urllib2.urlopen("https://gdata.youtube.com/feeds/api/videos/" + getYoutubeId(url) + "?v=2&alt=json")
        except urllib2.HTTPError:
            return None
        youtubeData = json.load(response)
        return youtubeData.get('entry').get('title').get("$t")
    return None


def cleanSoundcloudUrl(url):
    return url.split("#")[0]


def getYoutubeId(url):
    '''extract youtube id from url '''
    youtubeId = url[url.find("v=") + 2:]
    ampLoc = youtubeId.find("&")
    if ampLoc > -1:
        youtubeId = youtubeId[:ampLoc]
    return youtubeId


@app.route('/updatedb/<accessToken>', methods=['GET'])
def grabFeed(accessToken):
    '''facebook api returns a 400 error instead of json in case of invalid token'''
    try:
        groupFeed = json.load(urllib2.urlopen("https://graph.facebook.com/518171768298214/feed?limit=100&access_token=" + accessToken))
    except urllib2.HTTPError, e:
        results = {'success': False, 'reason': e.reason, 'code': e.code}
    else:
        results = []
        for post in groupFeed.get('data'):
            if post.get('link'):
                results.append({'url': post.get('link'), 'status': postSong(url=post.get('link'))})
        results = {'success': True, 'results': results}
    return jsonify(results)


@app.route('/updatedb', methods=['GET'])
def updatedb():
    return render_template("updatedb.html")


@socketio.on('connect')
def onConnect():
    pass
