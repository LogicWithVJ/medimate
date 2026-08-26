from datetime import datetime, timezone
from app.extensions import db


class Prescription(db.Model):
    """
    Represents one uploaded prescription file (image or PDF).

    This model only tracks the UPLOAD and its PREPROCESSED version.
    The extracted text (OCR) and structured medicine data (LLM output)
    will be added in later phases as separate models/columns, keeping
    raw upload data cleanly separated from AI-derived interpretation
    (medical safety requirement).
    """

    __tablename__ = "prescriptions"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)

    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False, unique=True)
    processed_filename = db.Column(db.String(255), nullable=True)
    file_type = db.Column(db.String(10), nullable=False)  # "image" or "pdf"

    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Status pipeline: "uploaded" -> "preprocessed" -> "ocr_done" -> "verified" (future)
    status = db.Column(db.String(30), nullable=False, default="uploaded")

    patient = db.relationship("Patient", backref="prescriptions")

    def __repr__(self):
        return f"<Prescription id={self.id} patient_id={self.patient_id} status={self.status}>"