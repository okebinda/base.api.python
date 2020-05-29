"""
Administrators module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint
from flask_principal import identity_loaded

from lib.auth import auth_basic
from modules.app_keys.middleware import require_appkey
from .routes_admin import get_administrators, post_administrator,\
    get_administrator, put_administrator, delete_administrator
from .authentication import Authentication


def register(app):
    """Register administrator routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    if app.config.get('APP_TYPE') == 'admin':
        admin_routes(app)


def admin_routes(app):
    """Register admin administrator routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    # pylint: disable=unused-variable

    @auth_basic.verify_password
    def verify_password(username_or_token, password):
        return Authentication.verify_password(username_or_token, password)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        return Authentication.on_identity_loaded(sender, identity)

    admin = Blueprint('admin_administrators', __name__)

    # GET /administrators
    admin.route("/administrators", methods=['GET'])(
    admin.route("/administrators/<int:page>", methods=['GET'])(
    admin.route("/administrators/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(  # noqa
        require_appkey(auth_basic.login_required(get_administrators)))))

    # POST /administrators
    admin.route('/administrators', methods=['POST'])(
        require_appkey(auth_basic.login_required(post_administrator)))

    # GET /administrator/{id}
    admin.route('/administrator/<int:administrator_id>', methods=['GET'])(
        require_appkey(auth_basic.login_required(get_administrator)))

    # PUT /administrator/{id}
    admin.route('/administrator/<int:administrator_id>', methods=['PUT'])(
        require_appkey(auth_basic.login_required(put_administrator)))

    # DELETE /administrator/{id}
    admin.route('/administrator/<int:administrator_id>', methods=['DELETE'])(
        require_appkey(auth_basic.login_required(delete_administrator)))

    app.register_blueprint(admin)
