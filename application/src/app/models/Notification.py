"""SQLAlchemy database record definition for Notification"""

from app import db
from app.lib.sqlalchemy.BaseModel import BaseModel


class Notification(db.Model, BaseModel):
    """Model for Notification"""

    __tablename__ = 'notifications'

    # columns
    user_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True)
    channel = db.Column(
        'channel',
        db.Integer,
        nullable=False)
    template = db.Column(
        'template',
        db.String(60),
        nullable=True)
    service = db.Column(
        'service',
        db.String(60),
        nullable=True)
    notification_id = db.Column(
        'notification_id',
        db.String(60),
        nullable=True)
    accepted = db.Column(
        'accepted',
        db.Integer,
        nullable=False)
    rejected = db.Column(
        'rejected',
        db.Integer,
        nullable=False)
    sent_at = db.Column(
        'sent_at',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False)

    # relationships
    user = db.relationship(
        'User',
        back_populates='notifications')
