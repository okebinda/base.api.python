"""
User Account module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from lib.auth import auth_basic
from modules.app_keys.middleware import require_appkey
from .routes_admin import get_account, put_account, put_password


def register(app):
    """Register user account routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)


def admin_routes(app):
    """Register admin user account routes with the application.

    :param app: Flask application
    :type app: Flask
    """

    admin = Blueprint('admin_user_account', __name__)

    # GET /user_account
    admin.route('/user_account', methods=['GET'])(
        require_appkey(auth_basic.login_required(get_account)))

    # PUT /user_account
    admin.route('/user_account', methods=['PUT'])(
        require_appkey(auth_basic.login_required(put_account)))

    # PUT /user_account/password
    admin.route('/user_account/password', methods=['PUT'])(
        require_appkey(auth_basic.login_required(put_password)))

    app.register_blueprint(admin)
