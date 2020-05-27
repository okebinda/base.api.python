"""
Logins module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long

from flask import Blueprint

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
    admin.route("/logins", methods=['GET'])(get_logins)
    admin.route("/logins/<int:page>", methods=['GET'])(get_logins)
    admin.route("/logins/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(get_logins)  # noqa

    app.register_blueprint(admin)
