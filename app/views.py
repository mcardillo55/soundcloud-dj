import urllib2
import json
from flask import render_template, request, jsonify
from app import app, db
from models import Song


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", songs=Song.query.all())


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


def postSong():
    url = request.json.get('url')
    title = findTitle(url)
    if title is None:
        data = {
            "success": False
        }
    else:
        if "youtube" in url:
            url = "//www.youtube.com/embed/" + getYoutubeId(url)
        newSong = Song(url=url, title=title)
        db.session.add(newSong)
        db.session.commit()
        data = {
            "success": True,
            "data": {
                "id": newSong.id,
                "url": newSong.url,
                "title": newSong.title
                }
        }
    print data
    return data


def findTitle(url):
    if "soundcloud" in url:
        try:
            response = urllib2.urlopen("http://soundcloud.com/oembed?url=" + url + "&format=json")
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


def getYoutubeId(url):
    '''extract youtube id from url '''
    youtubeId = url[url.find("v=") + 2:]
    ampLoc = youtubeId.find("&")
    if ampLoc > -1:
        youtubeId = youtubeId[:ampLoc]
    return youtubeId
