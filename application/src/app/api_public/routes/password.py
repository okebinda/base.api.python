import re
from datetime import datetime, timedelta
import time
import os
import hashlib

from flask import Blueprint, jsonify, request, g, current_app

from app import db
from app.models.User import User
from app.models.Role import Role
from app.models.PasswordReset import PasswordReset
from app.lib.random.String import String as RandomString
from app.lib.notify.Notify import Notify
from app.api_public.authentication import auth, user_permission, require_appkey
from app.api_public.schema.UserAccountSchema import UserAccountSchema

password = Blueprint('password', __name__)


@password.route('/user_account/password', methods=['PUT'])
@require_appkey
@auth.login_required
@user_permission.require(http_exception=403)
def put_password():

    # get user
    user = g.user

    # prep regex
    rePassword = re.compile(UserAccountSchema.rePassword)

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


@password.route('/password/request-reset-code', methods=['POST'])
@require_appkey
def post_password_request_reset_code():

    # initialize user
    user = None

    # validate data
    errors = {}
    if ('email' not in request.json or not request.json['email']):
        if ('email' not in errors):
            errors['email'] = []
        errors['email'].append("Missing data for required field.")
    if request.json.get('email'):
        temp_user = User(email=request.json.get('email'))
        if temp_user:
            user = User.query.filter(
                User.status == User.STATUS_ENABLED,
                User.roles.any(Role.id == 1),
                User.email_digest == temp_user.email_digest).first()
        if not user:
            if ('email' not in errors):
                errors['email'] = []
            errors['email'].append("Email address not found.")

    if (len(errors)):
        return jsonify({"error": errors}), 400

    # generate random seed
    d = datetime.now()
    unixtime = time.mktime(d.timetuple())
    hash_object = hashlib.sha256(
        (str(unixtime) + str(os.getpid()) + User.CRYPT_DIGEST_SALT).encode('utf-8'))
    random_seed = hash_object.hexdigest()

    # save reset request
    password_reset = PasswordReset(
        user_id=user.id,
        code=RandomString.user_code(8, random_seed),
        is_used=False,
        requested_at=datetime.now(),
        ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
        status=PasswordReset.STATUS_ENABLED,
        status_changed_at=datetime.now()
    )
    db.session.add(password_reset)
    db.session.commit()

    # email notification
    notify = Notify(current_app.config['ENV'], db)
    response = notify.send(user, Notify.CHANNEL_EMAIL, 'password-reset-code',
        name=user.profile.first_name if user.profile else 'User', code=password_reset.code)

    # response
    return jsonify({'success': 'true', 'sent': response}), 201


@password.route('/password/reset', methods=['PUT'])
@require_appkey
def put_password_reset():

    # initialize user
    user = None

    # prep regex
    rePassword = re.compile(UserAccountSchema.rePassword)

    # validate data
    errors = {}
    if ('code' not in request.json or not request.json['code']):
        if ('code' not in errors):
            errors['code'] = []
        errors['code'].append("Missing data for required field.")
    if ('email' not in request.json or not request.json['email']):
        if ('email' not in errors):
            errors['email'] = []
        errors['email'].append("Missing data for required field.")

    if request.json.get('email'):
        temp_user = User(email=request.json.get('email'))
        if temp_user:
            user = User.query.filter(
                User.status == User.STATUS_ENABLED,
                User.roles.any(Role.id == 1),
                User.email_digest == temp_user.email_digest).first()
        if not user:
            if ('email' not in errors):
                errors['email'] = []
            errors['email'].append("Email address not found.")
    if user and request.json.get('code'):
        password_reset = PasswordReset.query.filter(
            PasswordReset.status == PasswordReset.STATUS_ENABLED,
            PasswordReset.code == request.json.get('code'),
            PasswordReset.user_id == user.id,
            PasswordReset.is_used == False,
            (PasswordReset.requested_at + timedelta(seconds=3600)) >= datetime.now()
        ).first()
        if not password_reset:
            if ('code' not in errors):
                errors['code'] = []
            errors['code'].append("Invalid reset code.")

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

    # save password reset record
    password_reset.is_used = True
    
    # save user
    user.password = request.json.get('password1')
    db.session.commit()
    
    # response
    return jsonify({'success': 'true'}), 200
