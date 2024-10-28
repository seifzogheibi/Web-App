# from flask import Flask
# from CW1.app.models import db  # Import the database
# from CW1.app.views import views_bp  # Import the views blueprint

# def create_app():
#     app = Flask(__name__)  # Create the app instance

#     # Configuration settings from a separate config file
#     app.config.from_object('config.Config')  # Now we can configure the app

#     # Initialize the database with the app
#     db.init_app(app)

#     # Register the views blueprint to the app
#     app.register_blueprint(views_bp)

#     # Create database tables on app startup if they don't exist
#     with app.app_context():
#         db.create_all()

#     return app

# if __name__ == "__main__":
#     app = create_app()  # Create the app instance
#     app.run(debug=True)  # Run the app with debug mode enabled

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# app 

# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()  # Declare SQLAlchemy instance outside of app
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')  # Load your config
    
    db.init_app(app)  # Initialize db with app
    migrate.init_app(app, db)  # Initialize migration with the app and db

    with app.app_context():
        from . import views
        db.create_all()  # Create tables if they don't exist
    
    return app