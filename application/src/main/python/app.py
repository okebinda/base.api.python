"""
Application generator.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Flask

from init_dep import db, ma
from lib.wsgi import ReverseProxied
from lib import errors
from modules import health_check, locations, app_keys, roles, administrators, \
    terms_of_services, users, user_profiles, logins


def create_app(config):
    """Initializes the public application Flask object.

    :param config: Configuration ADT
    :type config: Config
    :returns: Flask app object
    """

    # init app
    app = Flask(__name__)
    app.config.from_object(config)

    # init database
    db.init_app(app)

    # init Marshmallow
    ma.init_app(app)

    # add support for URI versioning via web server
    app.wsgi_app = ReverseProxied(app.wsgi_app)

    # register error handlers
    errors.register(app)

    # register modules
    health_check.register(app)
    locations.register(app)
    app_keys.register(app)
    roles.register(app)
    administrators.register(app)
    terms_of_services.register(app)
    users.register(app)
    user_profiles.register(app)
    logins.register(app)

    return app
