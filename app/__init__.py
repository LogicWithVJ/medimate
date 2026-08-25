from flask import Flask
from config import Config
from app.extensions import db, login_manager


def create_app(config_class=Config):
    """Application factory: builds and returns a configured Flask app."""

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Bind extensions to this app instance
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Import models so SQLAlchemy knows about them before create_all() runs
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    # Tell Flask-Login how to load a user from the session
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.profile import profile_bp
    from app.routes.prescriptions import prescriptions_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(prescriptions_bp)

    @app.route("/")
    def home():
        return "MediMate is running! Go to /login or /register."

    return app