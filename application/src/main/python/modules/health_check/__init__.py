"""
Health check module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Blueprint

from .routes_public import get_health_check


def register(app):
    """Register health check routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public_routes(app)


def public_routes(app):
    """Register public health check routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public = Blueprint('public_health_check', __name__)

    # GET /health_check
    public.route("/health_check", methods=['GET'])(get_health_check)

    app.register_blueprint(public)
