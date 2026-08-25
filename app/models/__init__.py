"""
Makes 'models' a Python package.

Every model module is imported here so SQLAlchemy is aware of all
tables when create_app() runs db.create_all().
"""

from app.models.user import User
from app.models.patient import Patient
from app.models.caregiver import Caregiver
from app.models.prescription import Prescription

__all__ = ["User", "Patient", "Caregiver", "Prescription"]