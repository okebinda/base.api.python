"""
SQLAlchemy database record definitions for the Logins module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from init_dep import db


class Login(db.Model):
    """Model for Login"""

    __tablename__ = 'logins'

    API_ADMIN = 1
    API_PUBLIC = 2

    # columns
    id = db.Column(
        'id',
        db.BigInteger,
        primary_key=True)
    user_id = db.Column(
        'user_id',
        db.Integer,
        index=True,
        nullable=True)
    username = db.Column(
        'username',
        db.String(40),
        index=True,
        nullable=False)
    ip_address = db.Column(
        'ip_address',
        db.String(50),
        index=True)
    api = db.Column(
        'api',
        db.SmallInteger,
        nullable=False)
    success = db.Column(
        'success',
        db.Boolean,
        nullable=False)
    attempt_date = db.Column(
        'attempt_date',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False)

    # timestamps
    created_at = db.Column(
        'created_at',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False)
    updated_at = db.Column(
        'updated_at',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False)
