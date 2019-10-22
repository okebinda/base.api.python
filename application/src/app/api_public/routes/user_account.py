from datetime import datetime

from flask import Blueprint, jsonify, request, g
from marshmallow import ValidationError

from app import db
from app.models.User import User
from app.models.UserProfile import UserProfile
from app.models.Role import Role
from app.models.TermsOfService import TermsOfService
from app.models.UserTermsOfService import UserTermsOfService
from app.api_public.authentication import auth, user_permission, require_appkey, check_password_expiration
from app.api_public.schema.UserAccountSchema import UserAccountSchema


user_account = Blueprint('user_account', __name__)


@user_account.route('/user_account/step1', methods=['POST'])
@require_appkey
def post_user_account_step1():

    # init vars
    errors = {}

    # pre-validate data
    if request.json.get('username', None):
        user_query = User.query.filter(
            User.username == request.json.get('username')).first()
        if user_query:
            errors["username"] = ["Value must be unique."]

    if request.json.get('email', None):
        temp_user = User(email=request.json.get('email'))
        user_query = User.query.filter(
            User.email_digest == temp_user.email_digest).first()
        if user_query:
            errors["email"] = ["Value must be unique."]

    if request.json.get('password', None) and request.json.get('password2', None):
        if request.json.get('password') != request.json.get('password2'):
            errors['password2'] = ["Passwords must match."]

    if not request.json.get('tos_id', None):
        if ('tos_id' not in errors):
            errors['tos_id'] = []
        errors['tos_id'].append("Please agree to the terms of service.")
    if request.json.get('tos_id', None):
        tos = TermsOfService.query.get(request.json.get('tos_id'))
        if tos is None:
            if ('tos_id' not in errors):
                errors['tos_id'] = []
            errors['tos_id'].append("Invalid value.")

    # validate data
    try:
        data, _ = UserAccountSchema(
            strict=True,
            exclude=('first_name', 'last_name',)).load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user
    user = User(username=request.json.get('username').strip(),
                email=request.json.get('email').strip(),
                password=request.json.get('password'),
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
        terms_of_service_id=request.json.get('tos_id'),
        accept_date=datetime.now(),
        ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    db.session.add(user_tos)

    db.session.commit()

    # prep data
    data = {
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
    return jsonify({'user_account': UserAccountSchema().dump(data).data}), 201


@user_account.route('/user_account/step2', methods=['POST'])
@require_appkey
@auth.login_required
@user_permission.require(http_exception=403)
@check_password_expiration
def post_user_account_step2():

    # get user
    user = g.user

    # validate data
    try:
        data, _ = UserAccountSchema(
                strict=True,
                exclude=('username', 'email', 'password', 'password2', 'tos_id',)
            ).load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # save user profile
    user_profile = user.profile if user.profile else None
    if user_profile:
        user_profile.first_name = request.json.get('first_name', '').strip()
        user_profile.last_name = request.json.get('last_name', '').strip()

    else:
        user_profile = UserProfile(
            user_id=user.id,
            first_name=request.json.get('first_name', '').strip(),
            last_name=request.json.get('last_name', '').strip(),
            joined_at=datetime.now(),
            status=UserProfile.STATUS_ENABLED,
            status_changed_at=datetime.now())

        db.session.add(user_profile)

    db.session.commit()

    # prep data
    data = {
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
    return jsonify({'user_account': UserAccountSchema().dump(data).data}), 201


@user_account.route('/user_account', methods=['GET'])
@require_appkey
@auth.login_required
@user_permission.require(http_exception=403)
@check_password_expiration
def get_user_account():

    # get user
    user = g.user

    # prep data
    data = {
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
    return jsonify({'user_account': UserAccountSchema().dump(data).data}), 200


@user_account.route('/user_account', methods=['PUT'])
@require_appkey
@auth.login_required
@user_permission.require(http_exception=403)
@check_password_expiration
def put_user_account():

    # init vars
    user = g.user
    user_profile = user.profile if user.profile else None
    errors = {}

    # pre-validate data
    if request.json.get('username', None) and request.json.get('username') != user.username:
        user_query = User.query.filter(
            User.username == request.json.get('username')).first()
        if user_query:
            errors["username"] = ["Value must be unique."]

    if request.json.get('email', None) and request.json.get('email') != user.email:
        temp_user = User(email=request.json.get('email'))
        user_query = User.query.filter(
            User.email_digest == temp_user.email_digest).first()
        if user_query:
            errors["email"] = ["Value must be unique."]

    # validate data
    try:
        data, _ = UserAccountSchema(
                    strict=True,
                    exclude=('password', 'password2', 'tos_id',)).load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user
    user.username = request.json.get('username', '').strip()
    user.email = request.json.get('email', '').strip()

    # save user profile
    if user_profile:
        user_profile.first_name = request.json.get('first_name', '').strip()
        user_profile.last_name = request.json.get('last_name', '').strip()

    else:
        user_profile = UserProfile(
            user_id=user.id,
            first_name=request.json.get('first_name', '').strip(),
            last_name=request.json.get('last_name', '').strip(),
            joined_at=datetime.now(),
            status=UserProfile.STATUS_ENABLED,
            status_changed_at=datetime.now())

        db.session.add(user_profile)

    db.session.commit()

    # prep data
    data = {
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
    return jsonify({'user_account': UserAccountSchema().dump(data).data}), 200


@user_account.route('/user_account', methods=['DELETE'])
@require_appkey
@auth.login_required
@user_permission.require(http_exception=403)
@check_password_expiration
def delete_user_account():

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
