"""
Roles module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from lib.auth import auth_basic
from modules.app_keys.middleware import require_appkey
from .routes_admin import get_roles, post_roles, get_role, put_role, \
    delete_role


def register(app):
    """Register roles routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)


def admin_routes(app):
    """Register admin roles routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    admin = Blueprint('admin_roles', __name__)

    # GET /roles
    admin.route("/roles", methods=['GET'])(
    admin.route("/roles/<int:page>", methods=['GET'])(
    admin.route("/roles/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(  # noqa
    admin.route("/roles/<string:role_type>", methods=['GET'])(
    admin.route("/roles/<string:role_type>/<int:page>", methods=['GET'])(
    admin.route("/roles/<string:role_type>/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(  # noqa
        require_appkey(auth_basic.login_required(get_roles))))))))

    # POST /roles
    admin.route('/roles', methods=['POST'])(
        require_appkey(auth_basic.login_required(post_roles)))

    # GET /role/{id}
    admin.route('/role/<int:role_id>', methods=['GET'])(
    admin.route('/role/<string:name>', methods=['GET'])(  # noqa
        require_appkey(auth_basic.login_required(get_role))))

    # PUT /role/{id}
    admin.route('/role/<int:role_id>', methods=['PUT'])(
        require_appkey(auth_basic.login_required(put_role)))

    # DELETE /role/{id}
    admin.route('/role/<int:role_id>', methods=['DELETE'])(
        require_appkey(auth_basic.login_required(delete_role)))

    app.register_blueprint(admin)
