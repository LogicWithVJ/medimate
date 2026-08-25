from datetime import datetime, timezone
from app.extensions import db
from app.models.patient import patient_caregivers


class Caregiver(db.Model):
    """
    A caregiver profile linked one-to-one with a User account.
    Caregivers receive missed-dose escalation alerts (Phase 17)
    and view adherence dashboards (Phase 19-21) for their patients.
    """

    __tablename__ = "caregivers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    phone_number = db.Column(db.String(20), nullable=True)
    relationship_to_patient = db.Column(db.String(100), nullable=True)  # e.g. "daughter", "nurse"

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # One-to-one back to the User account
    user = db.relationship("User", backref=db.backref("caregiver_profile", uselist=False))

    # Many-to-many to patients, via the association table
    patients = db.relationship(
        "Patient",
        secondary=patient_caregivers,
        back_populates="caregivers",
    )

    def __repr__(self):
        return f"<Caregiver id={self.id} user_id={self.user_id}>"