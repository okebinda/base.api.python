"""
SQLAlchemy base model containing standard properties for most models to
inherit.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from init_dep import db


class BaseModel:
    """Base model containing: id, status, and timestamps"""

    STATUS_ENABLED = 1
    STATUS_DISABLED = 2
    STATUS_ARCHIVED = 3
    STATUS_DELETED = 4
    STATUS_PENDING = 5

    # properties
    id = db.Column(
        'id',
        db.Integer,
        primary_key=True)
    status = db.Column(
        'status',
        db.SmallInteger,
        nullable=False)

    # timestamps
    status_changed_at = db.Column(
        'status_changed_at',
        db.TIMESTAMP(timezone=True),
        nullable=False)
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
