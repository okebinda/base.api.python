"""
Authentication module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import datetime, timedelta
from functools import wraps

from flask import g, abort
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_principal import Permission, RoleNeed


auth_basic = HTTPBasicAuth()
auth_token = HTTPTokenAuth(scheme='Bearer')

permission_user = Permission(RoleNeed('USER'))
permission_super_admin = Permission(RoleNeed('SUPER_ADMIN'))


def check_password_expiration(view_function):
    """A Decorator function to check if the current user's password has
    expired.

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
