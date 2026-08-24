from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db


class User(UserMixin, db.Model):
    """
    Represents a person who can log into MediMate.

    UserMixin (from Flask-Login) adds the properties Flask-Login needs:
    is_authenticated, is_active, is_anonymous, and get_id().

    role distinguishes between the two account types MediMate supports:
    - "patient": the person taking medication
    - "caregiver": the person monitoring adherence and receiving alerts
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="patient")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, plain_password):
        """Hashes and stores the password. Never store plain text passwords."""
        self.password_hash = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        """Verifies a plain-text password against the stored hash."""
        return check_password_hash(self.password_hash, plain_password)

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"