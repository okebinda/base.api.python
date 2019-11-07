"""SQLAlchemy database record definition for User"""

import hashlib
from datetime import datetime
import bcrypt

from sqlalchemy.ext.hybrid import hybrid_property
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from app import db
from app.Config import Config
from app.lib.sqlalchemy.BaseModel import BaseModel
from app.lib.sqlalchemy.PGPString import PGPString
from app.models.PasswordReset import PasswordReset
from app.models.UserTermsOfService import UserTermsOfService
from app.models.Notification import Notification

# relation tables
roles = db.Table(
    'user_roles',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True),
    db.Column(
        'role_id',
        db.Integer,
        db.ForeignKey('roles.id'),
        primary_key=True)
)


class User(db.Model, BaseModel):
    """Model for User"""

    __tablename__ = 'users'

    HASH_ROUNDS = Config.AUTH_HASH_ROUNDS
    AUTH_SECRET_KEY = Config.AUTH_SECRET_KEY
    CRYPT_SYM_SECRET_KEY = Config.CRYPT_SYM_SECRET_KEY
    CRYPT_DIGEST_SALT = Config.CRYPT_DIGEST_SALT

    # columns
    _username = db.Column(
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
    _password = db.Column(
        'password',
        db.String(60),
        nullable=False)
    password_changed_at = db.Column(
        'password_changed_at',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False)
    is_verified = db.Column(
        'is_verified',
        db.Boolean,
        nullable=False)

    # relationships
    roles = db.relationship(
        'Role',
        secondary=roles,
        lazy='subquery',
        order_by="Role.priority",
        backref=db.backref('users', lazy=True))
    terms_of_services = db.relationship(
        'UserTermsOfService',
        lazy='subquery',
        cascade="all,delete-orphan",
        order_by=UserTermsOfService.accept_date.desc())
    password_resets = db.relationship(
        'PasswordReset ',
        cascade="all,delete-orphan",
        back_populates='user',
        order_by=PasswordReset.requested_at.desc())
    notifications = db.relationship(
        'Notification ',
        cascade="all,delete-orphan",
        back_populates='user',
        order_by=Notification.sent_at.desc())
    profile = db.relationship(
        'UserProfile',
        uselist=False,
        cascade="all,delete-orphan",
        back_populates='user')

    @hybrid_property
    def password(self):
        """Gets `password` property (hashed)

        :return: User's hashed password value
        :rtype: string
        """

        return self._password

    @password.setter
    def password(self, password):
        """Sets `password` property

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
    def username(self):
        """Gets `username` property

        :return: User's username
        :rtype: str
        """

        return self._username

    @username.setter
    def username(self, username):
        """Sets `username` property

        Strips leading and trailing whitespace and applies a lowercase
        transformation to `username` before storing it.

        :param username: User's username
        :type username: str
        """

        self._username = username.lower().strip()

    @hybrid_property
    def email(self):
        """Gets `email` property

        :return: User's plaintext email address
        :rtype: str
        """

        return self._email

    @email.setter
    def email(self, email):
        """Sets `email` property

        Applies a lowercase transformation to `email` before storing it. Also
        sets the `email_digest` property to its SHA-256 hash value - this is
        useful if the email is stored encrypted, to allow lookups and
        comparisons (e.g.: duplicates) if an exact match is supplied.

        :param email: User's plaintext email address
        :type email: str
        """

        self._email = email.lower().strip()
        hash_object = hashlib.sha256(
            (self.CRYPT_DIGEST_SALT + email).encode('utf-8'))
        self.email_digest = hash_object.hexdigest()

    def check_password(self, password):
        """Checks supplied password against saved value

        :param password: User's plaintext password
        :type password: str
        :return: True if password matches what's on file, False otherwise
        :rtype: bool
        """

        return bcrypt.checkpw(
            password.encode('utf-8'), self._password.encode('utf-8'))

    def generate_auth_token(self, expiration=1800):
        """Creates a new authentication token

        :param expiration: Length of time in seconds that token is valid
        :type expiration: int
        :return: Authentication token
        :rtype: str
        """

        s = Serializer(self.AUTH_SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id, 'type': 'user'})

    @staticmethod
    def verify_auth_token(token):
        """Verifies authentication token is valid and current

        :param token: Authentication token
        :type token: str
        :return: The user associated with token if valid, None otherwise
        :rtype: User | None
        """

        s = Serializer(User.AUTH_SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        if 'type' in data and data['type'] == 'user':
            user = User.query.get(data['id'])
            return user
        else:
            return None
