"""
Admin controllers for the User Account module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member

import re
from datetime import datetime
import bcrypt

from flask import jsonify, request, g
from marshmallow import ValidationError

from init_dep import db
from modules.administrators.model import Administrator, \
    AdministratorPasswordHistory
from modules.administrators.schema_admin import AdministratorAdminSchema
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


def put_password():
    """Updates the current user's password.

    :returns: JSON string of a `true` value; status code
    :rtype: (str, int)
    """
    # pylint: disable=too-many-branches

    # get user
    user = g.user

    # prep regex
    re_password = re.compile(AdministratorAdminSchema.re_password)

    # validate data
    errors = {}
    if ('previous_password' not in request.json or
            not request.json['previous_password']):
        if 'previous_password' not in errors:
            errors['previous_password'] = []
        errors['previous_password'].append("Missing data for required field.")
    elif ('previous_password' in request.json and
          not user.check_password(request.json['previous_password'])):
        if 'previous_password' not in errors:
            errors['previous_password'] = []
        errors['previous_password'].append("Incorrect password.")

    if 'password1' not in request.json or not request.json['password1']:
        if 'password1' not in errors:
            errors['password1'] = []
        errors['password1'].append("Missing data for required field.")
    if ('password1' in request.json and
            not re_password.match(request.json['password1'])):
        if 'password1' not in errors:
            errors['password1'] = []
        errors['password1'].append("Please choose a more complex password.")

    if 'password2' not in request.json or not request.json['password2']:
        if 'password2' not in errors:
            errors['password2'] = []
        errors['password2'].append("Missing data for required field.")
    if 'password1' in request.json and 'password2' in request.json:
        if request.json['password1'] != request.json['password2']:
            if 'password2' not in errors:
                errors['password2'] = []
            errors['password2'].append("New passwords must match.")

    if errors:
        return jsonify({"error": errors}), 400

    # check previous passwords
    if user.roles[0].password_policy and user.roles[0].password_reuse_history:
        prev_passwords = AdministratorPasswordHistory.query.\
            filter(AdministratorPasswordHistory.administrator_id == user.id).\
            order_by(AdministratorPasswordHistory.set_date.desc()).\
            limit(user.roles[0].password_reuse_history)
        for record in prev_passwords:
            print("TEST ", record.password)
            if bcrypt.checkpw(request.json.get('password1').encode('utf-8'),
                              record.password.encode('utf-8')):
                errors['password1'] = ["This password has recently been used."]
                break

    if errors:
        return jsonify({"error": errors}), 400

    # save user and password history
    user.password = request.json.get('password1')
    pass_history = AdministratorPasswordHistory(administrator=user,
                                                password=user.password,
                                                set_date=datetime.now())
    db.session.add(pass_history)
    db.session.commit()

    # response
    return jsonify({'success': 'true'}), 200
