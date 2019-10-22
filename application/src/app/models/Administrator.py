import bcrypt
import hashlib
from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from app import db
from app.Config import Config
from app.lib.sqlalchemy.BaseModel import BaseModel
from app.lib.sqlalchemy.PGPString import PGPString

# relation tables
roles = db.Table(
    'admin_roles',
    db.Column('admin_id', db.Integer, db.ForeignKey('administrators.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)


class Administrator(db.Model, BaseModel):

    __tablename__ = 'administrators'

    HASH_ROUNDS = Config.AUTH_HASH_ROUNDS
    AUTH_SECRET_KEY = Config.AUTH_SECRET_KEY
    CRYPT_SYM_SECRET_KEY = Config.CRYPT_SYM_SECRET_KEY
    CRYPT_DIGEST_SALT = Config.CRYPT_DIGEST_SALT

    # columns
    username = db.Column(
        'username', db.String(40), index=True, unique=True, nullable=False)
    _email = db.Column(
        'email', PGPString(CRYPT_SYM_SECRET_KEY, length=500), nullable=False)
    email_digest = db.Column(
        'email_digest', db.String(64), unique=True, nullable=False)
    first_name = db.Column(
        'first_name', PGPString(CRYPT_SYM_SECRET_KEY, length=200),
        nullable=False)
    last_name = db.Column(
        'last_name', PGPString(CRYPT_SYM_SECRET_KEY, length=200),
        nullable=False)
    _password = db.Column(
        'password', db.String(60), nullable=False)
    password_changed_at = db.Column(
        'password_changed_at', db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(), nullable=False)
    joined_at = db.Column(
        'joined_at', db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(), nullable=False)

    # relationships
    roles = db.relationship(
        'Role', secondary=roles, lazy='subquery',
        backref=db.backref('administrators', lazy=True))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = str(
            bcrypt.hashpw(
                bytes(password, 'utf-8'),
                bcrypt.gensalt(self.HASH_ROUNDS)),
            'utf8')
        self.password_changed_at = datetime.now()

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email.lower()
        hash_object = hashlib.sha256((self.CRYPT_DIGEST_SALT + email).encode('utf-8'))
        self.email_digest = hash_object.hexdigest()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self._password.encode('utf-8'))

    def generate_auth_token(self, expiration=1800):
        s = Serializer(self.AUTH_SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id, 'type': 'administrator'})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Administrator.AUTH_SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        if 'type' in data and data['type'] == 'administrator':
            admin = Administrator.query.get(data['id'])
            return admin
        else:
            return None
