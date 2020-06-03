"""
User Profiles module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from lib.auth import auth_basic, permission_super_admin, \
    check_password_expiration
from modules.app_keys.middleware import require_appkey
from .routes_admin import get_user_profiles, post_user_profiles,\
    get_user_profile, put_user_profile, delete_user_profile


def register(app):
    """Register user profile routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)


def admin_routes(app):
    """Register admin user profile routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    admin = Blueprint('admin_user_profiles', __name__)

    # GET /user_profiles
    admin.route("/user_profiles", methods=['GET'])(
    admin.route("/user_profiles/<int:page>", methods=['GET'])(
    admin.route("/user_profiles/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(  # noqa
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            get_user_profiles)))))))  # noqa

    # POST /user_profiles
    admin.route('/user_profiles', methods=['POST'])(
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            post_user_profiles)))))  # noqa

    # GET /user_profile/{id}
    admin.route('/user_profile/<int:user_profile_id>', methods=['GET'])(
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            get_user_profile)))))  # noqa

    # PUT /user_profile/{id}
    admin.route('/user_profile/<int:user_profile_id>', methods=['PUT'])(
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            put_user_profile)))))  # noqa

    # DELETE /user_profile/{id}
    admin.route('/user_profile/<int:user_profile_id>', methods=['DELETE'])(
        require_appkey(
        auth_basic.login_required(
        permission_super_admin.require(http_exception=403)(
        check_password_expiration(
            delete_user_profile)))))  # noqa

    app.register_blueprint(admin)
