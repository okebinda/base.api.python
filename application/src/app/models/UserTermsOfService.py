"""SQLAlchemy database record definition for UserTermsOfService"""

from app import db
from app.Config import Config
from app.lib.sqlalchemy.PGPString import PGPString


class UserTermsOfService(db.Model):
    """Model for UserTermsOfService"""

    __tablename__ = 'user_terms_of_services'

    CRYPT_SYM_SECRET_KEY = Config.CRYPT_SYM_SECRET_KEY

    # columns
    user_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True)
    terms_of_service_id = db.Column(
        'terms_of_service_id',
        db.Integer,
        db.ForeignKey('terms_of_services.id'),
        primary_key=True)
    accept_date = db.Column(
        'accept_date',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False)
    ip_address = db.Column(
        'ip_address',
        PGPString(CRYPT_SYM_SECRET_KEY, length=200),
        nullable=False)

    # relationships
    user = db.relationship(
        'User',
        uselist=False)
    terms_of_service = db.relationship(
        'TermsOfService',
        uselist=False)

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
