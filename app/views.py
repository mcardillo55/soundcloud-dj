import urllib2
import json
from flask import render_template, request, jsonify
from app import app, db
from models import Song

HOSTNAME = app.config['HOSTNAME']


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", songs=Song.query.all(), host=HOSTNAME)


@app.route('/api/playlist', methods=['GET', 'POST'])
def playlistAPI():
    if request.method == 'GET':
        data = getSongs()
    if request.method == 'POST':
        data = postSong()
    return jsonify(data)


def getSongs():
    songList = []
    for song in Song.query.all():
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
            return data
        data = {
            "success": True,
            "data": {
                "id": newSong.id,
                "url": newSong.url,
                "title": newSong.title
                }
        }
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
    groupFeed = json.load(urllib2.urlopen("https://graph.facebook.com/518171768298214/feed?limit=100&access_token=" + accessToken))
    for post in groupFeed.get('data'):
        if post.get('link'):
            postSong(url=post.get('link'))
            print post.get('link')
    return "Database updated!"


@app.route('/updatedb', methods=['GET'])
def updatedb():
    return render_template("updatedb.html")
