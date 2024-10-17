import os

class Config:
    SECRET_KEY = 'a-very-secret-secret'  # Secret key for session management and CSRF protection
    SQLALCHEMY_DATABASE_URI = 'sqlite:///assessments.db'  # Database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking