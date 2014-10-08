import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
CSRF_ENABLED = True
SECRET_KEY = 'this is a secret'
HOSTNAME = "http://127.0.0.1:5000"
PRODUCTION = False 
