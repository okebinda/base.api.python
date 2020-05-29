"""
Users module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from lib.auth import auth_basic
from modules.app_keys.middleware import require_appkey
from .routes_admin import get_users, post_user, get_user, put_user, delete_user


def register(app):
    """Register user routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)


def admin_routes(app):
    """Register admin user routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    admin = Blueprint('admin_users', __name__)

    # GET /users
    admin.route("/users", methods=['GET'])(
    admin.route("/users/<int:page>", methods=['GET'])(
    admin.route("/users/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(  # noqa
        require_appkey(auth_basic.login_required(get_users)))))

    # POST /users
    admin.route('/users', methods=['POST'])(
        require_appkey(auth_basic.login_required(post_user)))

    # GET /user/{id}
    admin.route('/user/<int:user_id>', methods=['GET'])(
    admin.route('/user/<string:username>', methods=['GET'])(  # noqa
        require_appkey(auth_basic.login_required(get_user))))

    # PUT /user/{id}
    admin.route('/user/<int:user_id>', methods=['PUT'])(
        require_appkey(auth_basic.login_required(put_user)))

    # DELETE /user/{id}
    admin.route('/user/<int:user_id>', methods=['DELETE'])(
        require_appkey(auth_basic.login_required(delete_user)))

    app.register_blueprint(admin)
