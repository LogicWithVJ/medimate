from flask import Flask
from config import Config


def create_app(config_class=Config):
    """Application factory: builds and returns a configured Flask app."""

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register a simple home route for now.
    # This will move into a Blueprint in a later step.
    @app.route("/")
    def home():
        return "MediMate is running!"

    return app