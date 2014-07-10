from config import SQLALCHEMY_DATABASE_URI
import os.path
from app import db

db.create_all()