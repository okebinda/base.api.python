"""
Users module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long

from flask import Blueprint
from flask_principal import identity_loaded

from lib.auth import auth_basic, permission_super_admin, permission_user, \
    check_password_expiration
from modules.app_keys.middleware import require_appkey
from .routes_auth import get_auth_token, get_auth_token_check
from .routes_admin import get_users, post_user, get_user, put_user, delete_user
from .authentication import Authentication


def register(app):
    """Register user routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)
    else:
        public_routes(app)


def public_routes(app):
    """Register public user routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    # pylint: disable=unused-variable

    @auth_basic.verify_password
    def verify_password(username_or_token, password):
        return Authentication.verify_password(username_or_token, password)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        return Authentication.on_identity_loaded(sender, identity)

    public = Blueprint('public_users', __name__)

    # GET /token
    public.route('/token', methods=['GET'])(
        require_appkey(
        auth_basic.login_required(
        permission_user.require(http_exception=403)(
            get_auth_token))))  # noqa

    # GET /token/check
    public.route('/token/check', methods=['GET'])(
        require_appkey(
        auth_basic.login_required(
        permission_user.require(http_exception=403)(
            get_auth_token_check))))  # noqa

    app.register_blueprint(public)


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
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            get_users)))))))  # noqa

    # POST /users
    admin.route('/users', methods=['POST'])(
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            post_user)))))  # noqa

    # GET /user/{id}
    admin.route('/user/<int:user_id>', methods=['GET'])(
    admin.route('/user/<string:username>', methods=['GET'])(  # noqa
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            get_user))))))  # noqa

    # PUT /user/{id}
    admin.route('/user/<int:user_id>', methods=['PUT'])(
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            put_user)))))  # noqa

    # DELETE /user/{id}
    admin.route('/user/<int:user_id>', methods=['DELETE'])(
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            delete_user)))))  # noqa

    app.register_blueprint(admin)
