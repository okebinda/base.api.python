"""
App Keys module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from lib.auth import auth_basic
from modules.app_keys.middleware import require_appkey
from .routes_admin import get_app_keys, post_app_keys, get_app_key, \
    put_app_key, delete_app_key


def register(app):
    """Register app keys routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)


def admin_routes(app):
    """Register admin app keys routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    admin = Blueprint('admin_app_keys', __name__)

    # GET /app_keys
    admin.route("/app_keys", methods=['GET'])(
    admin.route("/app_keys/<int:page>", methods=['GET'])(
    admin.route("/app_keys/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(  # noqa
        require_appkey(auth_basic.login_required(get_app_keys)))))

    # POST /app_keys
    admin.route('/app_keys', methods=['POST'])(
        require_appkey(auth_basic.login_required(post_app_keys)))

    # GET /app_key/{id}
    admin.route('/app_key/<int:app_key_id>', methods=['GET'])(
        require_appkey(auth_basic.login_required(get_app_key)))

    # PUT /app_key/{id}
    admin.route('/app_key/<int:app_key_id>', methods=['PUT'])(
        require_appkey(auth_basic.login_required(put_app_key)))

    # DELETE /app_key/{id}
    admin.route('/app_key/<int:app_key_id>', methods=['DELETE'])(
        require_appkey(auth_basic.login_required(delete_app_key)))

    app.register_blueprint(admin)
