"""
    __init__
    """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config.from_object('config')
# allow for images to be uploaded
app.config['UPLOAD_FOLDER'] = '/workspaces/Web-App/CW2/app/static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy()
db.init_app(app)


migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from app import models