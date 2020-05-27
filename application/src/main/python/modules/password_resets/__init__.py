"""
Password Resets module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long

from flask import Blueprint

from .routes_admin import get_password_resets


def register(app):
    """Register password resets routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)


def admin_routes(app):
    """Register admin password resets routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    admin = Blueprint('admin_password_resets', __name__)

    # GET /users
    admin.route("/password_resets", methods=['GET'])(get_password_resets)
    admin.route("/password_resets/<int:page>", methods=['GET'])(get_password_resets)  # noqa
    admin.route("/password_resets/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(get_password_resets)  # noqa

    app.register_blueprint(admin)
