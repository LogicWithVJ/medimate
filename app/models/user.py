from datetime import datetime, timezone
from app.extensions import db


class User(db.Model):
    """
    Represents a person who can log into MediMate.
    This will later be extended with roles (patient / caregiver)
    and linked to authentication in Phase 5.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"