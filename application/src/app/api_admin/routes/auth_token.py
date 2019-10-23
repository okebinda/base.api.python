"""Authentication Token controller"""

from flask import Blueprint, current_app, jsonify
from flask import g

from app.api_admin.authentication import auth, admin_permission, require_appkey

auth_token = Blueprint('auth_token', __name__)


@auth_token.route('/token', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
def get_auth_token():
    """Generates an authentication token

    :returns: JSON string of a token and some other information; status code
    :rtype: (str, int)
    """

    token = g.user.generate_auth_token(
        current_app.config['AUTH_TOKEN_EXPIRATION'])
    return jsonify(
        {'token': token.decode('ascii'), 'user_id': g.user.id,
         'expiration': current_app.config['AUTH_TOKEN_EXPIRATION']}), 200


@auth_token.route('/token/check', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
def get_auth_token_check():
    """Checks if an authentication token is still valid

    :returns: JSON string of a `true` value; status code
    :rtype: (str, int)
    """

    # response
    return jsonify({'token_check': True}), 200
