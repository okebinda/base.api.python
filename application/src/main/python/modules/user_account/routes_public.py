"""
Public controllers for the User Account module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member

import re
from datetime import datetime, timedelta
import time
import os
import hashlib
import bcrypt

from flask import jsonify, request, g, current_app
from marshmallow import ValidationError

from init_dep import db
from lib.schema.validate import unique, unique_email, exists
from lib.random import String as RandomString
from modules.users.model import User, UserTermsOfService, UserPasswordHistory
from modules.user_profiles.model import UserProfile
from modules.roles.model import Role
from modules.terms_of_services.model import TermsOfService
from modules.password_resets.model import PasswordReset
from modules.notifications.notify import Notify
from .schema_public import UserAccountSchema


def post_user_account_step1():
    """User registration step 1.

    :returns: JSON string of the user's account information; status code
    :rtype: (str, int)
    """

    # pre-validate data
    errors = unique({}, User, User.username,
                    str(request.json.get('username')).lower().strip()
                    if request.json.get('username', None) else None)

    errors = unique_email(errors, User, User.email,
                          str(request.json.get('email')).lower().strip()
                          if request.json.get('email', None) else None)

    errors, tos = exists(errors, TermsOfService, 'tos_id',
                         request.json.get('tos_id', None),
                         missing_error="Please agree to the terms of service.")

    if (request.json.get('password', None) and
            request.json.get('password2', None)):
        if request.json.get('password') != request.json.get('password2'):
            errors['password2'] = ["Passwords must match."]

    # validate data
    try:
        data = UserAccountSchema(
            exclude=('first_name', 'last_name',)).load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user
    user = User(username=data['username'].lower().strip(),
                email=data['email'].lower().strip(),
                password=data['password'],
                is_verified=False,
                status=User.STATUS_ENABLED,
                status_changed_at=datetime.now())

    user_role = Role.query.filter(Role.name == 'USER').first()
    if user_role:
        user.roles.append(user_role)

    db.session.add(user)

    # save user terms of service
    user_tos = UserTermsOfService(
        user=user,
        terms_of_service=tos,
        accept_date=datetime.now(),
        ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    db.session.add(user_tos)

    # save password history
    pass_history = UserPasswordHistory(
        user=user,
        password=user.password,
        set_date=datetime.now())
    db.session.add(pass_history)

    db.session.commit()

    # prep output
    output = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password_changed_at': user.password_changed_at,
        'is_verified': user.is_verified,
        'first_name': None,
        'last_name': None,
        'joined_at': None,
    }

    # response
    return jsonify(
        {'user_account': UserAccountSchema().dump(output)}), 201


def post_user_account_step2():
    """User registration step 2.

    :returns: JSON string of the user's account information; status code
    :rtype: (str, int)
    """

    # get user
    user = g.user

    # validate data
    try:
        data = UserAccountSchema(
            exclude=('username', 'email', 'password', 'password2', 'tos_id',)
        ).load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # save user profile
    user_profile = user.profile if user.profile else None
    if user_profile:
        user_profile.first_name = data['first_name'].strip()
        user_profile.last_name = data['last_name'].strip()

    else:
        user_profile = UserProfile(
            user_id=user.id,
            first_name=data['first_name'].strip(),
            last_name=data['last_name'].strip(),
            joined_at=datetime.now(),
            status=UserProfile.STATUS_ENABLED,
            status_changed_at=datetime.now())

        db.session.add(user_profile)

    db.session.commit()

    # prep output
    output = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password_changed_at': user.password_changed_at,
        'is_verified': user.is_verified,
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'joined_at': user_profile.joined_at,
    }

    # response
    return jsonify(
        {'user_account': UserAccountSchema().dump(output)}), 201


def get_user_account():
    """Retrieves user's account information.

    :returns: JSON string of the user's account information; status code
    :rtype: (str, int)
    """

    # get user
    user = g.user

    # prep output
    output = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password_changed_at': user.password_changed_at,
        'is_verified': user.is_verified,
        'first_name': user.profile.first_name if user.profile else None,
        'last_name': user.profile.last_name if user.profile else None,
        'joined_at': user.profile.joined_at if user.profile else None,
    }

    # response
    return jsonify(
        {'user_account': UserAccountSchema().dump(output)}), 200


def put_user_account():
    """Updates the current user's account information.

    :returns: JSON string of the user's account information; status code
    :rtype: (str, int)
    """

    # init vars
    user = g.user
    user_profile = user.profile if user.profile else None

    # pre-validate data
    errors = unique({}, User, User.username,
                    str(request.json.get('username')).lower().strip()
                    if request.json.get('username', None) else None,
                    update=user)

    errors = unique_email(errors, User, User.email,
                          str(request.json.get('email')).lower().strip()
                          if request.json.get('email', None) else None,
                          update=user)

    # validate data
    try:
        data = UserAccountSchema(
            exclude=('password', 'password2', 'tos_id',)).load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user
    user.username = data['username'].lower().strip()
    user.email = data['email'].lower().strip()

    # save user profile
    if user_profile:
        user_profile.first_name = data['first_name'].strip()
        user_profile.last_name = data['last_name'].strip()

    else:
        user_profile = UserProfile(
            user_id=user.id,
            first_name=data['first_name'].strip(),
            last_name=data['last_name'].strip(),
            joined_at=datetime.now(),
            status=UserProfile.STATUS_ENABLED,
            status_changed_at=datetime.now())

        db.session.add(user_profile)

    db.session.commit()

    # prep output
    output = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password_changed_at': user.password_changed_at,
        'is_verified': user.is_verified,
        'first_name': user_profile.first_name if user_profile else None,
        'last_name': user_profile.last_name if user_profile else None,
        'joined_at': user_profile.joined_at if user_profile else None,
    }

    # response
    return jsonify(
        {'user_account': UserAccountSchema().dump(output)}), 200


def delete_user_account():
    """Set's the current user's account to `delete` status.

    :returns: JSON string of the user's account information; status code
    :rtype: (str, int)
    """

    # get user
    user = g.user

    # delete post
    user.status = User.STATUS_DELETED
    user.status_changed_at = datetime.now()

    # delete user profile
    if user.profile:
        user.profile.status = UserProfile.STATUS_DELETED
        user.profile.status_changed_at = datetime.now()

    db.session.commit()

    # response
    return '', 204


def put_password():
    """Updates the current user's password.

    :returns: JSON string of a `true` value; status code
    :rtype: (str, int)
    """
    # pylint: disable=too-many-branches

    # get user
    user = g.user

    # prep regex
    re_password = re.compile(UserAccountSchema.re_password)

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
        prev_passwords = UserPasswordHistory.query.\
            filter(UserPasswordHistory.user_id == user.id).\
            order_by(UserPasswordHistory.set_date.desc()).\
            limit(user.roles[0].password_reuse_history)
        for record in prev_passwords:
            if bcrypt.checkpw(request.json.get('password1').encode('utf-8'),
                              record.password.encode('utf-8')):
                errors['password1'] = ["This password has recently been used."]
                break

    if errors:
        return jsonify({"error": errors}), 400

    # save user and password history
    user.password = request.json.get('password1')
    pass_history = UserPasswordHistory(user=user,
                                       password=user.password,
                                       set_date=datetime.now())
    db.session.add(pass_history)
    db.session.commit()

    # response
    return jsonify({'success': 'true'}), 200


def post_password_request_reset_code():
    """Creates a password reset code for the current user, send via email.

    :returns: JSON string of a `true` value; status code
    :rtype: (str, int)
    """

    # initialize user
    user = None

    # validate data
    errors = {}
    if 'email' not in request.json or not request.json['email']:
        if 'email' not in errors:
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
            if 'email' not in errors:
                errors['email'] = []
            errors['email'].append("Email address not found.")

    if errors:
        return jsonify({"error": errors}), 400

    # generate random seed
    now = datetime.now()
    unixtime = time.mktime(now.timetuple())
    hash_object = hashlib.sha256(
        (str(unixtime) + str(os.getpid()) +
         User.CRYPT_DIGEST_SALT).encode('utf-8'))
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
    response = notify.send(
        user,
        Notify.CHANNEL_EMAIL,
        'password-reset-code',
        name=user.profile.first_name if user.profile else 'User',
        code=password_reset.code)

    # response
    return jsonify({'success': 'true', 'sent': response}), 201


def put_password_reset():
    """Updates the current user's password using a reset code.

    :returns: JSON string of a `true` value; status code
    :rtype: (str, int)
    """
    # pylint: disable=too-many-branches

    # initialize user
    user = None

    # prep regex
    re_password = re.compile(UserAccountSchema.re_password)

    # validate data
    errors = {}
    if 'code' not in request.json or not request.json['code']:
        if 'code' not in errors:
            errors['code'] = []
        errors['code'].append("Missing data for required field.")
    if 'email' not in request.json or not request.json['email']:
        if 'email' not in errors:
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
            if 'email' not in errors:
                errors['email'] = []
            errors['email'].append("Email address not found.")
    if user and request.json.get('code'):
        password_reset = PasswordReset.query.filter(
            PasswordReset.status == PasswordReset.STATUS_ENABLED,
            PasswordReset.code == request.json.get('code'),
            PasswordReset.user_id == user.id,
            PasswordReset.is_used == False,  # noqa; pylint: disable=singleton-comparison
            (PasswordReset.requested_at +
             timedelta(seconds=3600)) >= datetime.now()
        ).first()
        if not password_reset:
            if 'code' not in errors:
                errors['code'] = []
            errors['code'].append("Invalid reset code.")

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

    # save password reset record
    password_reset.is_used = True

    # save user
    user.password = request.json.get('password1')
    db.session.commit()

    # response
    return jsonify({'success': 'true'}), 200
