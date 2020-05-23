"""
Roles module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long

from flask import Blueprint

from .routes_admin import get_roles, post_roles, get_role, put_role, \
    delete_role


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
    admin = Blueprint('admin_roles', __name__)

    # GET /roles
    admin.route("/roles", methods=['GET'])(get_roles)
    admin.route("/roles/<int:page>", methods=['GET'])(get_roles)
    admin.route("/roles/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(get_roles)  # noqa
    admin.route("/roles/<string:role_type>", methods=['GET'])(get_roles)
    admin.route("/roles/<string:role_type>/<int:page>", methods=['GET'])(get_roles)  # noqa
    admin.route("/roles/<string:role_type>/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(get_roles)  # noqa

    # POST /roles
    admin.route('/roles', methods=['POST'])(post_roles)

    # GET /role/{id}
    admin.route('/role/<int:role_id>', methods=['GET'])(get_role)
    admin.route('/role/<string:name>', methods=['GET'])(get_role)

    # PUT /role/{id}
    admin.route('/role/<int:role_id>', methods=['PUT'])(put_role)

    # DELETE /role/{id}
    admin.route('/role/<int:role_id>', methods=['DELETE'])(delete_role)

    app.register_blueprint(admin)
