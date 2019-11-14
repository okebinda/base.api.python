"""User Account controller"""

from flask import Blueprint, jsonify, request, g
from marshmallow import ValidationError

from app import db
from app.models.Administrator import Administrator
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.UserAccountSchema import UserAccountSchema

user_account = Blueprint('user_account', __name__)


@user_account.route('/user_account', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_account():
    """Retrieves user's account information

    :returns: JSON string of the user's account information; status code
    :rtype: (str, int)
    """

    # get user
    user = g.user

    # response
    return jsonify({'user_account': UserAccountSchema().dump(user)}), 200


@user_account.route('/user_account', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def put_account():
    """Updates the current user's account information

    :returns: JSON string of the user's account information; status code
    :rtype: (str, int)
    """

    # init vars
    user = g.user
    errors = {}

    # pre-validate data
    if (request.json.get('username', None) and
            request.json.get('username') != user.username):
        administrator_query = Administrator.query.filter(
            Administrator.username == request.json.get('username')).first()
        if administrator_query:
            errors["username"] = ["Value must be unique."]
    if (request.json.get('email', None) and
            request.json.get('email') != user.email):
        temp_admin = Administrator(email=request.json.get('email'))
        administrator_query = Administrator.query.filter(
            Administrator.email_digest == temp_admin.email_digest).first()
        if administrator_query:
            errors["email"] = ["Value must be unique."]

    # validate data
    try:
        data = UserAccountSchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user account
    user.username = data['username'].strip()
    user.email = data['email'].strip()
    user.first_name = data['first_name'].strip()
    user.last_name = data['last_name'].strip()

    db.session.commit()

    # response
    return jsonify({'user_account': UserAccountSchema().dump(user)}), 200
