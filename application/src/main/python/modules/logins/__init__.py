"""
Logins module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from modules.app_keys.middleware import require_appkey
from .routes_admin import get_logins


def register(app):
    """Register login routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)


def admin_routes(app):
    """Register admin login routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    admin = Blueprint('admin_logins', __name__)

    # GET /users
    admin.route("/logins", methods=['GET'])(
    admin.route("/logins/<int:page>", methods=['GET'])(
    admin.route("/logins/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(  # noqa
        require_appkey(get_logins))))

    app.register_blueprint(admin)
