from config import DB_PATH
import os.path
from app import db

try:
    os.makedirs(os.path.split(DB_PATH)[0])
except:
    print("DB_PATH already exists, not creating...")
    pass

db.create_all()
