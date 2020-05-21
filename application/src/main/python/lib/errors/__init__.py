"""
Error handling module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from .handlers import error_400, error_401, error_403, error_404, error_405, \
    error_500


def register(app):
    """Register error handlers with the application.

    :param app: Flask application
    :type app: Flask
    """
    app.errorhandler(400)(error_400)
    app.errorhandler(401)(error_401)
    app.errorhandler(403)(error_403)
    app.errorhandler(404)(error_404)
    app.errorhandler(405)(error_405)
    app.errorhandler(500)(error_500)
