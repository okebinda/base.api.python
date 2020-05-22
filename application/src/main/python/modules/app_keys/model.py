"""
SQLAlchemy database record definitions for App Keys module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from init_dep import db
from lib.sqlalchemy.base_model import BaseModel


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
