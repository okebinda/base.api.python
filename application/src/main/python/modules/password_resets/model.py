"""
SQLAlchemy database record definitions for the Logins module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from init_dep import db
from lib.sqlalchemy.base_model import BaseModel


class PasswordReset(db.Model, BaseModel):
    """Model for PasswordReset"""

    __tablename__ = 'password_resets'

    # columns
    user_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    code = db.Column(
        'code',
        db.String(40),
        nullable=False)
    is_used = db.Column(
        'is_used',
        db.Boolean,
        nullable=False)
    requested_at = db.Column(
        'requested_at',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False)
    ip_address = db.Column(
        'ip_address',
        db.String(50),
        index=True)

    # relationships
    user = db.relationship(
        'User',
        back_populates='password_resets')
