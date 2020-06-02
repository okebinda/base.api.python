"""
User Account module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from lib.auth import auth_basic, permission_user, permission_super_admin
from modules.app_keys.middleware import require_appkey
from modules.users.authentication import check_password_expiration
from .routes_public import post_user_account_step1, post_user_account_step2, \
    get_user_account, put_user_account, delete_user_account, \
    put_password as public_put_password, post_password_request_reset_code, \
    put_password_reset
from .routes_admin import get_account, put_account, put_password


def register(app):
    """Register user account routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)
    else:
        public_routes(app)


def public_routes(app):
    """Register public user account routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    # pylint: disable=unused-variable

    public = Blueprint('public_user_account', __name__)

    # POST /user_account/step1
    public.route('/user_account/step1', methods=['POST'])(
        require_appkey(
            post_user_account_step1))

    # POST /user_account/step2
    public.route('/user_account/step2', methods=['POST'])(
        require_appkey(
        auth_basic.login_required(
        permission_user.require(http_exception=403)(
        check_password_expiration(
            post_user_account_step2)))))  # noqa

    # GET /user_account
    public.route('/user_account', methods=['GET'])(
        require_appkey(
        auth_basic.login_required(
        permission_user.require(http_exception=403)(
        check_password_expiration(
            get_user_account)))))  # noqa

    # PUT /user_account
    public.route('/user_account', methods=['PUT'])(
        require_appkey(
        auth_basic.login_required(
        permission_user.require(http_exception=403)(
        check_password_expiration(
            put_user_account)))))  # noqa

    # DELETE /user_account
    public.route('/user_account', methods=['DELETE'])(
        require_appkey(
        auth_basic.login_required(
        permission_user.require(http_exception=403)(
        check_password_expiration(
            delete_user_account)))))  # noqa

    # PUT /user_account/password
    public.route('/user_account/password', methods=['PUT'])(
        require_appkey(
        auth_basic.login_required(
        permission_user.require(http_exception=403)(
        check_password_expiration(
            public_put_password)))))  # noqa

    # POST /password/request-reset-code
    public.route('/password/request-reset-code', methods=['POST'])(
        require_appkey(
            post_password_request_reset_code))

    # PUT /password/reset
    public.route('/password/reset', methods=['PUT'])(
        require_appkey(
            put_password_reset))

    app.register_blueprint(public)


def admin_routes(app):
    """Register admin user account routes with the application.

    :param app: Flask application
    :type app: Flask
    """

    admin = Blueprint('admin_user_account', __name__)

    # GET /user_account
    admin.route('/user_account', methods=['GET'])(
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            get_account)))))  # noqa

    # PUT /user_account
    admin.route('/user_account', methods=['PUT'])(
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            put_account)))))  # noqa

    # PUT /user_account/password
    admin.route('/user_account/password', methods=['PUT'])(
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            put_password)))))  # noqa

    app.register_blueprint(admin)
