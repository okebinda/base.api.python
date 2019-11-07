"""Password controller"""

import re
from datetime import datetime
import bcrypt

from flask import Blueprint, jsonify, request
from flask import g

from app import db
from app.api_admin.authentication import auth, admin_permission, require_appkey
from app.api_admin.schema.AdministratorSchema import AdministratorSchema
from app.models.AdministratorPasswordHistory import AdministratorPasswordHistory

password = Blueprint('password', __name__)


@password.route('/user_account/password', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
def put_password():
    """Updates the current user's password

    :returns: JSON string of a `true` value; status code
    :rtype: (str, int)
    """

    # get user
    user = g.user

    # prep regex
    re_password = re.compile(AdministratorSchema.re_password)

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
        prev_passwords = AdministratorPasswordHistory.query.filter(
            AdministratorPasswordHistory.administrator_id == user.id).order_by(
            AdministratorPasswordHistory.set_date.desc()).limit(
            user.roles[0].password_reuse_history)
        for record in prev_passwords:
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
