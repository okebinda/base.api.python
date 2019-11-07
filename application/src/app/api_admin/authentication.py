"""A collection of helper functions and a class for API security"""

from datetime import datetime, timedelta
from functools import wraps

from flask import g, current_app, request, abort
from flask_httpauth import HTTPBasicAuth
from flask_principal import Identity, Permission, RoleNeed, UserNeed,\
    identity_changed
from sqlalchemy.orm.exc import NoResultFound

from app import db
from app.models.Administrator import Administrator
from app.models.Login import Login
from app.models.Role import Role
from app.models.AppKey import AppKey

auth = HTTPBasicAuth()
user_permission = Permission(RoleNeed('USER'))
admin_permission = Permission(RoleNeed('SUPER_ADMIN'))


def require_appkey(view_function):
    """A Decorator function to check a request endpoint for a valid
    application key

    :param view_function: The function to decorate
    :type view_function: function
    :return: The internal decorator function
    :rtype: function
    """
    # pylint: disable=inconsistent-return-statements

    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        """Internal decorator function"""

        if request.args.get('app_key'):
            try:
                AppKey.query.filter(
                    AppKey.key == request.args.get('app_key'),
                    AppKey.status == AppKey.STATUS_ENABLED).one()
            except NoResultFound:
                abort(401, "Bad application key")
            return view_function(*args, **kwargs)
        else:
            abort(401, "Missing application key")
    return decorated_function


def check_password_expiration(view_function):
    """A Decorator function to check if the current user's password has
    expired

    :param view_function: The function to decorate
    :type view_function: function
    :return: The internal decorator function
    :rtype: function
    """

    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        """Internal decorator function"""

        if hasattr(g, 'user'):
            password_valid_window = g.user.password_changed_at + timedelta(
                days=g.user.roles[0].password_reset_days)
            pvw = password_valid_window.replace(tzinfo=None)
            if pvw < datetime.now():
                abort(403, "Password expired")
        return view_function(*args, **kwargs)
    return decorated_function


class Authentication:
    """Helper class for administrator authentication"""

    @staticmethod
    def verify_password(username_or_token, password):
        """Verifies that the requested user's password matches what is on file
        or that the access token is valid, and that the user's account is not
        locked

        :param username_or_token: The user's username or access token
        :type username_or_token: str
        :param password: The user's password
        :type password: str
        :return: True on success or abort on failure
        :rtype: bool
        """

        # first try to authenticate by token
        user = Administrator.verify_auth_token(username_or_token)
        if not user:

            # ADMIN login lockout policy
            if Authentication.is_account_locked(username_or_token):
                abort(401, "Account locked")

            # try to authenticate with username/password
            user = Administrator.query.filter(
                Administrator.username == username_or_token,
                Administrator.status == Administrator.STATUS_ENABLED).first()
            if not user or not user.check_password(password):

                # log failed login
                if password:
                    login_record = Login(
                        user_id=user.id if user else None,
                        username=username_or_token[0:40],
                        ip_address=request.environ.get('HTTP_X_REAL_IP',
                                                       request.remote_addr),
                        api=Login.API_ADMIN,
                        success=False,
                        attempt_date=datetime.now())
                    db.session.add(login_record)
                    db.session.commit()

                # fail
                abort(401, "Bad credentials")
            else:

                # log successful login
                login_record = Login(
                    user_id=user.id,
                    username=username_or_token[0:40],
                    ip_address=request.environ.get('HTTP_X_REAL_IP',
                                                   request.remote_addr),
                    api=Login.API_ADMIN,
                    success=True,
                    attempt_date=datetime.now())
                db.session.add(login_record)
                db.session.commit()

        # set global user
        g.user = user

        # Tell Flask-Principal the identity changed
        # pylint: disable=protected-access
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(user.id))
        return True

    @staticmethod
    def on_identity_loaded(sender, identity):
        """Initialize user with roles

        :param sender:
        :param identity:
        """
        # pylint: disable=unused-argument

        # Set the identity user object
        if hasattr(g, 'user'):
            identity.user = g.user

            # Add the UserNeed to the identity
            if hasattr(g.user, 'id'):
                identity.provides.add(UserNeed(g.user.id))

            # Assuming the User model has a list of roles, update the
            # identity with the roles that the user provides
            if hasattr(g.user, 'roles'):
                for role in g.user.roles:
                    identity.provides.add(RoleNeed(role.name))

    @staticmethod
    def is_account_locked(username_or_token):
        """Checks if user's account has been locked

        :param username_or_token: The user's username or access token
        :type username_or_token: str
        :return: True if locked or False if available
        :rtype: bool
        """

        admin_role = Role.query.filter(Role.name == 'SUPER_ADMIN').first()
        if admin_role.login_lockout_policy:
            login_query = Login.query
            if admin_role.login_ban_by_ip:
                login_query = login_query.filter(
                    Login.username == username_or_token,
                    Login.ip_address == request.environ.get(
                        'HTTP_X_REAL_IP', request.remote_addr))
            else:
                login_query = login_query.filter(
                    Login.username == username_or_token)
            recent_logins = login_query.order_by(
                Login.attempt_date.desc()).limit(admin_role.login_max_attempts)
            if recent_logins.count() >= admin_role.login_max_attempts:
                if sum(list(map(
                        lambda x: 1 if not x.success else 0, recent_logins
                ))) >= admin_role.login_max_attempts:
                    if ((recent_logins[0].attempt_date -
                         recent_logins[-1].attempt_date).total_seconds() <=
                            admin_role.login_timeframe):
                        banned_window = recent_logins[0].attempt_date + \
                                        timedelta(
                                            seconds=admin_role.login_ban_time)
                        bw = banned_window.replace(tzinfo=None)
                        if bw > datetime.now():
                            return True
        return False
