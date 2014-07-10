from flask import render_template, request, jsonify
from app import app, db
from forms import SubmissionForm
from models import Song

@app.route('/', methods = ['GET', 'POST'])
def hello():
	form = SubmissionForm()
	if form.validate_on_submit():
		db.session.add(Song(url=form.data['subURL']))
		db.session.commit()
		return "Success!"
	return render_template("index.html", form=form, songs=Song.query.all())

@app.route('/api/playlist', methods = ['GET', 'POST'])
def playlistAPI():
	if request.method == 'GET':
		data = getSongs()
	if request.method == 'POST':
		data = postSong()
	return jsonify(data)

def getSongs():
	songList = []
	for song in Song.query.all():
		songDict = {"id": song.id, "url": song.url}
		songList.append(songDict.copy())
	data = {
		"songList": songList
	}
	return data

def postSong():
	url = request.json.get('url')
	db.session.add(Song(url=url))
	db.session.commit()
	data = {
		"success": True
	}
	return data