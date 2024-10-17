from flask import Flask
from models import db  # Import the database
from views import views_bp  # Import the views blueprint

def create_app():
    app = Flask(__name__)  # Create the app instance

    # Configuration settings from a separate config file
    app.config.from_object('config.Config')  # Now we can configure the app

    # Initialize the database with the app
    db.init_app(app)

    # Register the views blueprint to the app
    app.register_blueprint(views_bp)

    # Create database tables on app startup if they don't exist
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()  # Create the app instance
    app.run(debug=True)  # Run the app with debug mode enabled
