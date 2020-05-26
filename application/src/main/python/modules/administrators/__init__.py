"""
Administrators module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long

from flask import Blueprint

from .routes_admin import get_administrators, post_administrator,\
    get_administrator, put_administrator, delete_administrator


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
    admin = Blueprint('admin_administrators', __name__)

    # GET /administrators
    admin.route("/administrators", methods=['GET'])(get_administrators)
    admin.route("/administrators/<int:page>", methods=['GET'])(get_administrators)  # noqa
    admin.route("/administrators/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(get_administrators)  # noqa

    # POST /administrators
    admin.route('/administrators', methods=['POST'])(post_administrator)

    # GET /administrator/{id}
    admin.route('/administrator/<int:administrator_id>', methods=['GET'])(get_administrator)  # noqa

    # PUT /administrator/{id}
    admin.route('/administrator/<int:administrator_id>', methods=['PUT'])(put_administrator)  # noqa

    # DELETE /administrator/{id}
    admin.route('/administrator/<int:administrator_id>', methods=['DELETE'])(delete_administrator)  # noqa

    app.register_blueprint(admin)
