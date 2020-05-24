"""
SQLAlchemy database record definitions for Administrators module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

import hashlib
from datetime import datetime

# from main import app
import bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from init_dep import db
from config import Config
from lib.sqlalchemy.base_model import BaseModel
from lib.sqlalchemy.pgp_string import PGPString


# relation tables
roles = db.Table(
    'admin_roles',
    db.Column(
        'admin_id',
        db.Integer,
        db.ForeignKey('administrators.id'),
        primary_key=True),
    db.Column(
        'role_id',
        db.Integer,
        db.ForeignKey('roles.id'),
        primary_key=True)
)


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


class Administrator(db.Model, BaseModel):
    """Model for Administrator"""

    __tablename__ = 'administrators'

    HASH_ROUNDS = Config.AUTH_HASH_ROUNDS
    AUTH_SECRET_KEY = Config.AUTH_SECRET_KEY
    CRYPT_SYM_SECRET_KEY = Config.CRYPT_SYM_SECRET_KEY
    CRYPT_DIGEST_SALT = Config.CRYPT_DIGEST_SALT

    # columns
    username = db.Column(
        'username',
        db.String(40),
        index=True,
        unique=True,
        nullable=False)
    _email = db.Column(
        'email',
        PGPString(CRYPT_SYM_SECRET_KEY, length=500),
        nullable=False)
    email_digest = db.Column(
        'email_digest',
        db.String(64),
        unique=True,
        nullable=False)
    first_name = db.Column(
        'first_name',
        PGPString(CRYPT_SYM_SECRET_KEY, length=200),
        nullable=False)
    last_name = db.Column(
        'last_name',
        PGPString(CRYPT_SYM_SECRET_KEY, length=200),
        nullable=False)
    _password = db.Column(
        'password',
        db.String(60),
        nullable=False)
    password_changed_at = db.Column(
        'password_changed_at',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False)
    joined_at = db.Column(
        'joined_at',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False)

    # relationships
    roles = db.relationship(
        'Role',
        secondary=roles,
        lazy='subquery',
        order_by="Role.priority",
        backref=db.backref('administrators', lazy=True))
    password_history = db.relationship(
        'AdministratorPasswordHistory',
        cascade="all,delete-orphan",
        back_populates='administrator',
        order_by=AdministratorPasswordHistory.set_date.desc())

    @hybrid_property
    def password(self):
        """Gets `password` property (hashed).

        :return: User's hashed password value
        :rtype: string
        """

        return self._password

    @password.setter
    def password(self, password):
        """Sets `password` property.

        Applies Bcrypt hashing function to `password` before storing it. The
        number of hashing rounds are configurable in the main application
        config settings.

        :param password: User's plaintext password
        :type password: str
        """

        self._password = str(
            bcrypt.hashpw(
                bytes(password, 'utf-8'),
                bcrypt.gensalt(self.HASH_ROUNDS)),
            'utf8')
        self.password_changed_at = datetime.now()

    @hybrid_property
    def email(self):
        """Gets `email` property.

        :return: User's plaintext email address
        :rtype: str
        """

        return self._email

    @email.setter
    def email(self, email):
        """Sets `email` property.

        Applies a lowercase transformation to `email` before storing it. Also
        sets the `email_digest` property to its SHA-256 hash value - this is
        useful if the email is stored encrypted, to allow lookups and
        comparisons (e.g.: duplicates) if an exact match is supplied.

        :param email: User's plaintext email address
        :type email: str
        """

        self._email = email.lower()
        hash_object = hashlib.sha256(
            (self.CRYPT_DIGEST_SALT + email).encode('utf-8'))
        self.email_digest = hash_object.hexdigest()

    def check_password(self, password):
        """Checks supplied password against saved value.

        :param password: User's plaintext password
        :type password: str
        :return: True if password matches what's on file, False otherwise
        :rtype: bool
        """

        return bcrypt.checkpw(
            password.encode('utf-8'), self._password.encode('utf-8'))

    def generate_auth_token(self, expiration=1800):
        """Creates a new authentication token.

        :param expiration: Length of time in seconds that token is valid
        :type expiration: int
        :return: Authentication token
        :rtype: str
        """

        s = Serializer(self.AUTH_SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id, 'type': 'administrator'})

    @staticmethod
    def verify_auth_token(token):
        """Verifies authentication token is valid and current.

        :param token: Authentication token
        :type token: str
        :return: The user associated with token if valid, None otherwise
        :rtype: User | None
        """

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
