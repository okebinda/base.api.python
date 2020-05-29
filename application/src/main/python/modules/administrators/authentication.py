"""
Authentication for Administrators module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member

from datetime import datetime, timedelta

from flask import g, current_app, request, abort
from flask_principal import Identity, RoleNeed, UserNeed, identity_changed

from init_dep import db
from modules.logins.model import Login
from modules.roles.model import Role
from .model import Administrator


# auth = HTTPBasicAuth()
# admin_permission = Permission(RoleNeed('SUPER_ADMIN'))


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
                        ban_win = banned_window.replace(tzinfo=None)
                        if ban_win > datetime.now():
                            return True
        return False
