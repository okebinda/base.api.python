"""
Administrators module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=line-too-long,bad-continuation

from flask import Blueprint

from modules.app_keys.middleware import require_appkey
from .routes_admin import get_administrators, post_administrator,\
    get_administrator, put_administrator, delete_administrator


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
    admin = Blueprint('admin_administrators', __name__)

    # GET /administrators
    admin.route("/administrators", methods=['GET'])(
    admin.route("/administrators/<int:page>", methods=['GET'])(
    admin.route("/administrators/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])(  # noqa
        require_appkey(get_administrators))))

    # POST /administrators
    admin.route('/administrators', methods=['POST'])(
        require_appkey(post_administrator))

    # GET /administrator/{id}
    admin.route('/administrator/<int:administrator_id>', methods=['GET'])(
        require_appkey(get_administrator))

    # PUT /administrator/{id}
    admin.route('/administrator/<int:administrator_id>', methods=['PUT'])(
        require_appkey(put_administrator))

    # DELETE /administrator/{id}
    admin.route('/administrator/<int:administrator_id>', methods=['DELETE'])(
        require_appkey(delete_administrator))

    app.register_blueprint(admin)
