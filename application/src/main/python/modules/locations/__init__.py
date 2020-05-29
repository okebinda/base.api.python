"""
Locations module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from modules.app_keys.middleware import require_appkey
from .routes_public import get_countries, get_regions


def register(app):
    """Register locations routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') != 'admin':
        public_routes(app)


def public_routes(app):
    """Register locations check routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public = Blueprint('public_locations', __name__)

    # GET /health_check
    public.route("/countries", methods=['GET'])(
    public.route("/countries/<int:page>", methods=['GET'])(
    public.route("/countries/<int:page>/<int(min=1, max=250):limit>", methods=['GET'])(  # noqa
        require_appkey(get_countries))))

    # GET /regions
    public.route("/regions/<string:country_code>", methods=['GET'])(
    public.route("/regions/<string:country_code>/<int:page>", methods=['GET'])(
    public.route("/regions/<string:country_code>/<int:page>/<int(min=1, max=250):limit>", methods=['GET'])(  # noqa
        require_appkey(get_regions))))

    app.register_blueprint(public)
