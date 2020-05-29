"""
Notifications module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from lib.auth import auth_basic
from modules.app_keys.middleware import require_appkey
from .routes_admin import get_notifications


def register(app):
    """Register notifications routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)


def admin_routes(app):
    """Register admin notifications routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    admin = Blueprint('admin_notifications', __name__)

    # GET /users
    admin.route("/notifications", methods=['GET'])(
    admin.route("/notifications/<int:page>", methods=['GET'])(
    admin.route("/notifications/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(  # noqa
        require_appkey(auth_basic.login_required(get_notifications)))))

    app.register_blueprint(admin)
