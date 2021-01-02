"""
SQLAlchemy database record definitions for the User Profiles module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from lib.sqlalchemy.base_model import BaseModel
from lib.sqlalchemy.pgp_string import PGPString
from init_dep import db
from config import Config


class UserProfile(db.Model, BaseModel):
    """Model for UserProfile"""

    __tablename__ = 'user_profiles'

    CRYPT_SYM_SECRET_KEY = Config.CRYPT_SYM_SECRET_KEY

    # columns
    user_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    first_name = db.Column(
        'first_name',
        PGPString(CRYPT_SYM_SECRET_KEY, length=200),
        nullable=False)
    last_name = db.Column(
        'last_name',
        PGPString(CRYPT_SYM_SECRET_KEY, length=200),
        nullable=False)
    joined_at = db.Column(
        'joined_at',
        db.TIMESTAMP(timezone=True),
        index=True,
        server_default=db.func.current_timestamp(),
        nullable=False)

    # relationships
    user = db.relationship(
        'User',
        back_populates='profile')
