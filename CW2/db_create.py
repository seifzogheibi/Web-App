"""
    Database
    """
from CW2.config import SQLALCHEMY_DATABASE_URI
from app import db

db.create_all()
