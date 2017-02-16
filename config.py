import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
CSRF_ENABLED = True
SECRET_KEY = 'this is a secret'
HOSTNAME = "http://127.0.0.1:5000"
PRODUCTION = False
YOUTUBE_API_KEY = 'API_KEY_GOES_HERE'
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/videos/'
SOUNDCLOUD_API_URL = 'http://soundcloud.com/oembed'
