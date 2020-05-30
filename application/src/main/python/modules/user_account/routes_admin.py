"""
Admin controllers for the User Account module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member

from flask import jsonify, request, g
from marshmallow import ValidationError

from init_dep import db
from modules.administrators.model import Administrator
from lib.schema.validate import unique, unique_email
from .schema_admin import UserAccountAdminSchema


def get_account():
    """Retrieves user's account information.

    :returns: JSON string of the user's account information; status code
    :rtype: (str, int)
    """

    # get user
    user = g.user

    # response
    return jsonify({'user_account': UserAccountAdminSchema().dump(user)}), 200


def put_account():
    """Updates the current user's account information.

    :returns: JSON string of the user's account information; status code
    :rtype: (str, int)
    """

    # init vars
    user = g.user

    # pre-validate data
    errors = unique({}, Administrator, Administrator.username,
                    request.json.get('username', None), update=user)

    errors = unique_email(errors, Administrator, Administrator.email,
                          request.json.get('email', None), update=user)

    # validate data
    try:
        data = UserAccountAdminSchema().load(request.json)
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
    return jsonify({'user_account': UserAccountAdminSchema().dump(user)}), 200
