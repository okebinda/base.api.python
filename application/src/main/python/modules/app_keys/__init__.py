"""
App Keys module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long

from flask import Blueprint

from .routes_admin import get_app_keys, post_app_keys, get_app_key, \
    put_app_key, delete_app_key


def register(app):
    """Register health check routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    admin_routes(app)


def admin_routes(app):
    """Register admin health check routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    admin = Blueprint('admin_app_keys', __name__)

    # GET /app_keys
    admin.route("/app_keys", methods=['GET'])(get_app_keys)
    admin.route("/app_keys/<int:page>", methods=['GET'])(get_app_keys)
    admin.route("/app_keys/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(get_app_keys)  # noqa

    # POST /app_keys
    admin.route('/app_keys', methods=['POST'])(post_app_keys)

    # GET /app_key/{id}
    admin.route('/app_key/<int:app_key_id>', methods=['GET'])(get_app_key)

    # PUT /app_key/{id}
    admin.route('/app_key/<int:app_key_id>', methods=['PUT'])(put_app_key)

    # DELETE /app_key/{id}
    admin.route('/app_key/<int:app_key_id>', methods=['DELETE'])(delete_app_key)  # noqa

    app.register_blueprint(admin)
