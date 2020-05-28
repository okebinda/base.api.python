"""
Middleware for App Keys module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from functools import wraps

from flask import request, abort
from sqlalchemy.orm.exc import NoResultFound

from .model import AppKey


def require_appkey(view_function):
    """A Decorator function to check a request endpoint for a valid
    application key.

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
        abort(401, "Missing application key")
    return decorated_function
