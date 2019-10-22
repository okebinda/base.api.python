from app import db
from app.lib.sqlalchemy.BaseModel import BaseModel
from app.lib.sqlalchemy.PGPString import PGPString
from app.Config import Config


class UserProfile(db.Model, BaseModel):

    __tablename__ = 'user_profiles'

    CRYPT_SYM_SECRET_KEY = Config.CRYPT_SYM_SECRET_KEY

    # columns
    user_id = db.Column(
        'user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(
        'first_name', PGPString(CRYPT_SYM_SECRET_KEY, length=200),
        nullable=False)
    last_name = db.Column(
        'last_name', PGPString(CRYPT_SYM_SECRET_KEY, length=200),
        nullable=False)
    joined_at = db.Column(
        'joined_at', db.TIMESTAMP(timezone=True), index=True,
        server_default=db.func.current_timestamp(), nullable=False)

    # relationships
    user = db.relationship('User', back_populates='profile')
