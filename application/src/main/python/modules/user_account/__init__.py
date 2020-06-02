"""
User Account module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from lib.auth import auth_basic
from modules.app_keys.middleware import require_appkey
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
        require_appkey(post_user_account_step1))

    # POST /user_account/step2
    public.route('/user_account/step2', methods=['POST'])(
        require_appkey(auth_basic.login_required(post_user_account_step2)))

    # GET /user_account
    public.route('/user_account', methods=['GET'])(
        require_appkey(auth_basic.login_required(get_user_account)))

    # PUT /user_account
    public.route('/user_account', methods=['PUT'])(
        require_appkey(auth_basic.login_required(put_user_account)))

    # DELETE /user_account
    public.route('/user_account', methods=['DELETE'])(
        require_appkey(auth_basic.login_required(delete_user_account)))

    # PUT /user_account/password
    public.route('/user_account/password', methods=['PUT'])(
        require_appkey(auth_basic.login_required(public_put_password)))

    # POST /password/request-reset-code
    public.route('/password/request-reset-code', methods=['POST'])(
        require_appkey(
            auth_basic.login_required(post_password_request_reset_code)))

    # PUT /password/reset
    public.route('/password/reset', methods=['PUT'])(
        require_appkey(auth_basic.login_required(put_password_reset)))

    app.register_blueprint(public)


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
