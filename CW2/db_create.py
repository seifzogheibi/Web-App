from CW2.config import SQLALCHEMY_DATABASE_URI
from CW2.app import db
import os.path

db.create_all()
