from app import db
from app.lib.sqlalchemy import BaseModel

class Notification(db.Model, BaseModel):

    __tablename__ = 'notifications'

    # columns
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    channel = db.Column(db.Integer, nullable=False)
    template = db.Column(db.String(60), nullable=True)
    service = db.Column(db.String(60), nullable=True)
    notification_id = db.Column(db.String(60), nullable=True)
    accepted = db.Column(db.Integer, nullable=False)
    rejected = db.Column(db.Integer, nullable=False)
    sent_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
        nullable=False)

    # relationships
    user = db.relationship('User', back_populates='notifications')
