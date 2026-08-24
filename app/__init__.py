from flask import Flask
from config import Config
from app.extensions import db


def create_app(config_class=Config):
    """Application factory: builds and returns a configured Flask app."""

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Bind SQLAlchemy to this app instance
    db.init_app(app)

    # Import models so SQLAlchemy knows about them before create_all() runs
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    # Simple home route for now.
    @app.route("/")
    def home():
        return "MediMate is running!"

    return app