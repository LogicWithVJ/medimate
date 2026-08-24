"""
Makes 'models' a Python package.

Every model module (user.py, patient.py, etc.) will be imported here
so that SQLAlchemy is aware of all tables when create_app() runs.
"""

from app.models.user import User

__all__ = ["User"]