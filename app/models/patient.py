from datetime import datetime, timezone
from app.extensions import db

# Association table for the many-to-many relationship between
# patients and caregivers. A patient can have several caregivers,
# and a caregiver can monitor several patients.
patient_caregivers = db.Table(
    "patient_caregivers",
    db.Column("patient_id", db.Integer, db.ForeignKey("patients.id"), primary_key=True),
    db.Column("caregiver_id", db.Integer, db.ForeignKey("caregivers.id"), primary_key=True),
)


class Patient(db.Model):
    """
    A patient profile linked one-to-one with a User account.
    Holds medically-relevant identity info (not medical history —
    that lives in Prescription/Medicine models added in later phases).
    """

    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    date_of_birth = db.Column(db.Date, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    emergency_contact_name = db.Column(db.String(150), nullable=True)
    emergency_contact_phone = db.Column(db.String(20), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # One-to-one back to the User account
    user = db.relationship("User", backref=db.backref("patient_profile", uselist=False))

    # Many-to-many to caregivers, via the association table
    caregivers = db.relationship(
        "Caregiver",
        secondary=patient_caregivers,
        back_populates="patients",
    )

    def __repr__(self):
        return f"<Patient id={self.id} user_id={self.user_id}>"