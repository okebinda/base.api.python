"""SQLAlchemy database record definition for UserPasswordHistory"""

from app import db


class UserPasswordHistory(db.Model):
    """Model for UserPasswordHistory"""

    __tablename__ = 'user_password_history'

    # columns
    id = db.Column(
        'id',
        db.BigInteger,
        primary_key=True)
    user_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True)
    password = db.Column(
        'password',
        db.String(60),
        nullable=False)
    set_date = db.Column(
        'set_date',
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

    # relationships
    user = db.relationship(
        'User',
        back_populates='password_history')
