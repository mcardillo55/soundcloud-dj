from flask import render_template, request, jsonify
from app import app
from app.models import Song


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", songs=Song.query.all())


@app.route("/api/playlist", methods=["GET"])
@app.route("/api/playlist/<int:start>", methods=["GET"])
def playlist_api(start=None):
    data = get_songs(start)
    return jsonify(data)


def get_songs(start=None):
    """Grabs 50 songs at once, optionally starting at id < start."""
    if start:
        query = (
            Song.query.order_by(Song.id.desc())
            .filter(Song.id < start)
            .limit(50)
            .all()
        )
    else:
        query = Song.query.order_by(Song.id.desc()).limit(50).all()

    song_list = [{"id": s.id, "url": s.url, "title": s.title} for s in query]
    return {"songList": song_list}
