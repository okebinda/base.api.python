"""
Terms of Services module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from modules.app_keys.middleware import require_appkey
from .routes_public import get_terms_of_service as public_get_terms_of_service
from .routes_admin import get_terms_of_services, post_terms_of_services,\
    get_terms_of_service, put_terms_of_service, delete_terms_of_service


def register(app):
    """Register terms of services routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)
    else:
        public_routes(app)


def public_routes(app):
    """Register public terms of services routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public = Blueprint('public_terms_of_services', __name__)

    # GET /terms_of_service/current
    public.route("/terms_of_service/current", methods=['GET'])(
        require_appkey(public_get_terms_of_service))

    app.register_blueprint(public)


def admin_routes(app):
    """Register admin terms of services routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    admin = Blueprint('admin_terms_of_services', __name__)

    # GET /terms_of_services
    admin.route("/terms_of_services", methods=['GET'])(
    admin.route("/terms_of_services/<int:page>", methods=['GET'])(
    admin.route("/terms_of_services/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(  # noqa
        require_appkey(get_terms_of_services))))

    # POST /terms_of_services
    admin.route('/terms_of_services', methods=['POST'])(
        require_appkey(post_terms_of_services))

    # GET /terms_of_service/{id}
    admin.route('/terms_of_service/<int:terms_of_service_id>', methods=['GET'])(  # noqa
        require_appkey(get_terms_of_service))

    # PUT /terms_of_service/{id}
    admin.route('/terms_of_service/<int:terms_of_service_id>', methods=['PUT'])(  # noqa
        require_appkey(put_terms_of_service))

    # DELETE /terms_of_service/{id}
    admin.route('/terms_of_service/<int:terms_of_service_id>', methods=['DELETE'])(  # noqa
        require_appkey(delete_terms_of_service))

    app.register_blueprint(admin)
