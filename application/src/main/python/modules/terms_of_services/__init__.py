"""
Terms of Services module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long

from flask import Blueprint

from .routes_admin import get_terms_of_services, post_terms_of_services,\
    get_terms_of_service, put_terms_of_service, delete_terms_of_service


def register(app):
    """Register terms of services routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)


def admin_routes(app):
    """Register admin terms of services routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    admin = Blueprint('admin_terms_of_services', __name__)

    # GET /terms_of_services
    admin.route("/terms_of_services", methods=['GET'])(get_terms_of_services)
    admin.route("/terms_of_services/<int:page>", methods=['GET'])(get_terms_of_services)  # noqa
    admin.route("/terms_of_services/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(get_terms_of_services)  # noqa

    # POST /terms_of_services
    admin.route('/terms_of_services', methods=['POST'])(post_terms_of_services)

    # GET /terms_of_service/{id}
    admin.route('/terms_of_service/<int:terms_of_service_id>', methods=['GET'])(get_terms_of_service)  # noqa

    # PUT /terms_of_service/{id}
    admin.route('/terms_of_service/<int:terms_of_service_id>', methods=['PUT'])(put_terms_of_service)  # noqa

    # DELETE /terms_of_service/{id}
    admin.route('/terms_of_service/<int:terms_of_service_id>', methods=['DELETE'])(delete_terms_of_service)  # noqa

    app.register_blueprint(admin)
