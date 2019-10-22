import re

from flask import Blueprint, jsonify, request
from flask import g

from app import db
from app.api_admin.authentication import auth, admin_permission, require_appkey
from app.api_admin.schema import AdministratorSchema

password = Blueprint('password', __name__)

@password.route('/account/password', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
def put_password():

    # get user
    user = g.user

    # prep regex
    rePassword = re.compile(AdministratorSchema.rePassword)

    # validate data
    errors = {}
    if ('previous_password' not in request.json or not request.json['previous_password']):
        if ('previous_password' not in errors):
            errors['previous_password'] = []
        errors['previous_password'].append("Missing data for required field.")
    elif 'previous_password' in request.json and not user.check_password(request.json['previous_password']):
        if ('previous_password' not in errors):
            errors['previous_password'] = []
        errors['previous_password'].append("Incorrect password.")

    if ('password1' not in request.json or not request.json['password1']):
        if ('password1' not in errors):
            errors['password1'] = []
        errors['password1'].append("Missing data for required field.")
    if ('password1' in request.json and not rePassword.match(request.json['password1'])):
        if ('password1' not in errors):
            errors['password1'] = []
        errors['password1'].append("Please choose a more complex password.")

    if ('password2' not in request.json or not request.json['password2']):
        if ('password2' not in errors):
            errors['password2'] = []
        errors['password2'].append("Missing data for required field.")
    if ('password1' in request.json and 'password2' in request.json):
        if (request.json['password1'] != request.json['password2']):
            if ('password2' not in errors):
                errors['password2'] = []
            errors['password2'].append("New passwords must match.")
    
    if (len(errors)):
        return jsonify({"error": errors}), 400

    # save user
    user.password = request.json.get('password1')
    db.session.commit()

    # response
    return jsonify({'success': 'true'}), 200
