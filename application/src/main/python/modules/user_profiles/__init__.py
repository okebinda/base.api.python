"""
User Profiles module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long

from flask import Blueprint

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
    admin.route("/user_profiles", methods=['GET'])(get_user_profiles)
    admin.route("/user_profiles/<int:page>", methods=['GET'])(get_user_profiles)  # noqa
    admin.route("/user_profiles/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(get_user_profiles)  # noqa

    # POST /user_profiles
    admin.route('/user_profiles', methods=['POST'])(post_user_profiles)

    # GET /user_profile/{id}
    admin.route('/user_profile/<int:user_profile_id>', methods=['GET'])(get_user_profile)  # noqa

    # PUT /user_profile/{id}
    admin.route('/user_profile/<int:user_profile_id>', methods=['PUT'])(put_user_profile)  # noqa

    # DELETE /user_profile/{id}
    admin.route('/user_profile/<int:user_profile_id>', methods=['DELETE'])(delete_user_profile)  # noqa

    app.register_blueprint(admin)
