"""SQLAlchemy database record definition for PasswordReset"""

from app import db
from app.lib.sqlalchemy.BaseModel import BaseModel


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
