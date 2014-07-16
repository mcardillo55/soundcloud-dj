import urllib2
import json
from flask import render_template, request, jsonify
from app import app, db
from forms import SubmissionForm
from models import Song


@app.route('/', methods=['GET', 'POST'])
def hello():
    form = SubmissionForm()
    if form.validate_on_submit():
        db.session.add(Song(url=form.data['subURL']))
        db.session.commit()
        return "Success!"
    return render_template("index.html", form=form, songs=Song.query.all())


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
    return data


def findTitle(url):
    if "soundcloud" in url:
        response = urllib2.urlopen("http://soundcloud.com/oembed?url=" + url + "&format=json")
        soundcloudData = json.load(response)
        return soundcloudData.get('title')
    elif "youtube" in url:
        response = urllib2.urlopen("https://gdata.youtube.com/feeds/api/videos/" + getYoutubeId(url) + "?v=2&alt=json")
        youtubeData = json.load(response)
        return youtubeData.get('entry').get('title').get("$t")


def getYoutubeId(url):
    '''extract youtube id from url '''
    youtubeId = url[url.find("v=") + 2:]
    ampLoc = youtubeId.find("&")
    if ampLoc > -1:
        youtubeId = youtubeId[:ampLoc]
    return youtubeId
