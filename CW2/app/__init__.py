# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask import Flask,request, session
# from flask_admin import Admin
# from flask_babel import Babel

# def get_locale():
#     if request.args.get('lang'):
#         session['lang'] = request.args.get('lang')
#     return session.get('lang', 'en')

# app = Flask(__name__)
# babel = Babel(app, locale_selector=get_locale)
# admin = Admin(app,template_mode='bootstrap4')
# app.config.from_object('config')
# db = SQLAlchemy(app)

# migrate = Migrate(app, db)

# from app import views, models


# Set Up Login Manager:
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy()
db.init_app(app)


migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to the login page for unauthorized users

from app.models import User  # Import your User model

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from app import views, models