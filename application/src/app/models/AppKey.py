"""SQLAlchemy database record definition for AppKey"""

from app import db
from app.lib.sqlalchemy.BaseModel import BaseModel


class AppKey(db.Model, BaseModel):
    """Model for AppKey"""

    __tablename__ = 'app_keys'

    # columns
    application = db.Column(
        'application',
        db.String(200),
        unique=True,
        nullable=False)
    key = db.Column(
        'key',
        db.String(32),
        index=True,
        unique=True,
        nullable=False)
