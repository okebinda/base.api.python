from app import db
from app.lib.sqlalchemy.BaseModel import BaseModel


class PasswordReset(db.Model, BaseModel):

    __tablename__ = 'password_resets'

    # columns
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column(db.String(40), nullable=False)
    is_used = db.Column(db.Boolean, nullable=False)
    requested_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(),
        nullable=False)
    ip_address = db.Column(db.String(50), index=True)

    # relationships
    user = db.relationship('User', back_populates='password_resets')
