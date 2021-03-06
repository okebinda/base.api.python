"""
Application generator.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Flask
from flask_principal import Principal
from flask_cors import CORS

from init_dep import db, ma, logger
from lib.wsgi import ReverseProxied
from lib import errors
from modules import health_check, locations, app_keys, roles, administrators, \
    terms_of_services, users, user_profiles, logins, password_resets, \
    notifications, user_account


def create_app(config):
    """Initializes the public application Flask object.

    :param config: Configuration ADT
    :type config: Config
    :returns: Flask app object
    """

    # init app
    app = Flask(__name__)
    app.config.from_object(config)

    # init logging
    logger.init_app(app)

    # init authorization
    Principal(app)

    # init CORS
    if 'CORS_ORIGIN' in app.config:
        CORS(app, supports_credentials=True,
             resources={r"/*": {"origins": app.config['CORS_ORIGIN']}})

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
    password_resets.register(app)
    notifications.register(app)
    user_account.register(app)

    return app
