"""
Locations module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from lib.auth import auth_basic
from modules.app_keys.middleware import require_appkey
from .routes_public import \
    get_countries as public_get_countries, \
    get_regions as public_get_regions
from .routes_admin import \
    get_countries as admin_get_countries, \
    get_regions as admin_get_regions


def register(app):
    """Register locations routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)
    else:
        public_routes(app)


def public_routes(app):
    """Register locations routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public = Blueprint('public_locations', __name__)

    # GET /health_check
    public.route("/countries", methods=['GET'])(
    public.route("/countries/<int:page>", methods=['GET'])(
    public.route("/countries/<int:page>/<int(min=1, max=250):limit>", methods=['GET'])(  # noqa
        require_appkey(public_get_countries))))

    # GET /regions
    public.route("/regions/<string:country_code>", methods=['GET'])(
    public.route("/regions/<string:country_code>/<int:page>", methods=['GET'])(
    public.route("/regions/<string:country_code>/<int:page>/<int(min=1, max=250):limit>", methods=['GET'])(  # noqa
        require_appkey(public_get_regions))))

    app.register_blueprint(public)


def admin_routes(app):
    """Register admin lcoations routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    admin = Blueprint('admin_locations', __name__)

    # GET /countries
    admin.route("/countries", methods=['GET'])(
    admin.route("/countries/<int:page>", methods=['GET'])(
    admin.route("/countries/<int:page>/<int(min=1, max=250):limit>", methods=['GET'])(  # noqa
        require_appkey(auth_basic.login_required(admin_get_countries)))))

    # GET /countries
    admin.route("/regions", methods=['GET'])(
    admin.route("/regions/<int:page>", methods=['GET'])(
    admin.route("/regions/<int:page>/<int(min=1, max=250):limit>", methods=['GET'])(  # noqa
        require_appkey(auth_basic.login_required(admin_get_regions)))))

    app.register_blueprint(admin)
