"""
Users module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long

from flask import Blueprint

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
    admin.route("/users", methods=['GET'])(get_users)
    admin.route("/users/<int:page>", methods=['GET'])(get_users)
    admin.route("/users/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(get_users)  # noqa

    # POST /users
    admin.route('/users', methods=['POST'])(post_user)

    # GET /user/{id}
    admin.route('/user/<int:user_id>', methods=['GET'])(get_user)
    admin.route('/user/<string:username>', methods=['GET'])(get_user)

    # PUT /user/{id}
    admin.route('/user/<int:user_id>', methods=['PUT'])(put_user)

    # DELETE /user/{id}
    admin.route('/user/<int:user_id>', methods=['DELETE'])(delete_user)

    app.register_blueprint(admin)
