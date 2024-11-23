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


app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy()
db.init_app(app)


migrate = Migrate(app, db)

from app import views, models


