"""
Central place for Flask extension instances.

We create extension objects here (without binding them to an app yet)
so they can be imported anywhere in the project without causing
circular imports. They get bound to the actual app inside create_app().
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()