"""
SQLAlchemy database record definitions for the Terms of Service module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from init_dep import db
from lib.sqlalchemy.base_model import BaseModel


class TermsOfService(db.Model, BaseModel):
    """Model for TermsOfService"""

    __tablename__ = 'terms_of_services'

    # columns
    text = db.Column(
        'text',
        db.Text(),
        nullable=False)
    version = db.Column(
        'version',
        db.String(10),
        unique=True,
        nullable=False)
    publish_date = db.Column(
        'publish_date',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False)
