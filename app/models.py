from app import db

class Song(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(255), index = True, unique = True)
    title = db.Column(db.String(255), index = True, unique = False)