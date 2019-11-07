"""SQLAlchemy database record definition for AdministratorPasswordHistory"""

from app import db


class AdministratorPasswordHistory(db.Model):
    """Model for AdministratorPasswordHistory"""

    __tablename__ = 'administrator_password_history'

    # columns
    id = db.Column(
        'id',
        db.BigInteger,
        primary_key=True)
    administrator_id = db.Column(
        'administrator_id',
        db.Integer,
        db.ForeignKey('administrators.id'),
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
    administrator = db.relationship(
        'Administrator',
        back_populates='password_history')
