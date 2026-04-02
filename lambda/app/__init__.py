import os
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
url_prefix = os.environ.get("URL_PREFIX", "").rstrip("/")
db_path = os.path.join(basedir, "db", "app.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["HOSTNAME"] = url_prefix  # used in templates for asset/API URLs

# Open SQLite in read-only mode via URI connection
def _readonly_creator():
    uri = "file:{}?mode=ro".format(db_path)
    return sqlite3.connect(uri, uri=True)


try:
    # SQLAlchemy 2.x / Flask-SQLAlchemy 3.x
    from sqlalchemy import event as _sa_event

    db = SQLAlchemy(app, engine_options={"creator": _readonly_creator})
except TypeError:
    # Fallback for older SQLAlchemy on dev machines — plain connection (not read-only)
    db = SQLAlchemy(app)

from app import views  # noqa: E402, F401
