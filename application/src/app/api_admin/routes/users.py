"""Users controller"""

from datetime import datetime

from flask import Blueprint, jsonify, abort, request, url_for
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from app import db
from app.models.User import User
from app.models.Role import Role
from app.models.UserProfile import UserProfile
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.UserSchema import UserSchema

users = Blueprint('users', __name__)


@users.route("/users", methods=['GET'])
@users.route("/users/<int:page>", methods=['GET'])
@users.route("/users/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_users(page=1, limit=10):
    """Retrieves a list of users

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of users; status code
    :rtype: (str, int)
    """

    # initialize query
    user_query = User.query

    # filter query based on URL parameters
    if request.args.get('status', '').isnumeric():
        user_query = user_query.filter(
            User.status == int(request.args.get('status')))
    else:
        user_query = user_query.filter(
            User.status.in_((User.STATUS_ENABLED, User.STATUS_DISABLED,
                             User.STATUS_PENDING)))

    if request.args.get('role', '').isnumeric():
        user_query = user_query.filter(
            User.roles.any(Role.id == int(request.args.get('role'))))

    # initialize order options dict
    order_options = {
        'id.asc': User.id.asc(),
        'id.desc': User.id.desc(),
        'username.asc': User.username.asc(),
        'username.desc': User.username.desc(),
    }

    # determine order
    if request.args.get('order_by') in order_options:
        order_by = order_options[request.args.get('order_by')]
    else:
        order_by = User.id.asc()

    # retrieve and return results
    results = user_query.order_by(order_by).limit(limit).offset(
        (page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'users': UserSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': user_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'users.get_users', page=page - 1, limit=limit, _external=True,
                order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'users.get_users', page=page + 1, limit=limit, _external=True,
                order_by=request.args.get('order_by', None))
        return jsonify(output), 200
    else:
        return '', 204


@users.route('/users', methods=['POST'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def post_user():
    """Creates a new user

    :returns: JSON string of the new user's data; status code
    :rtype: (str, int)
    """

    # init vars
    errors = {}
    roles = []

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

    if not request.json.get('roles', None):
        errors["roles"] = ["Missing data for required field."]
    else:
        for role_id in request.json.get('roles'):
            role = Role.query.get(role_id)
            if role is None:
                errors["roles"] = ["Invalid value."]
            else:
                roles.append(role.id)

    # validate data
    try:
        data = UserSchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user
    user = User(username=data['username'].strip(),
                email=data['email'].strip(),
                password=data['password'],
                is_verified=data['is_verified'],
                status=data['status'],
                status_changed_at=datetime.now())

    for role_id in roles:
        role = Role.query.get(role_id)
        user.roles.append(role)

    # save user profile
    if 'profile' in data:
        user_profile = UserProfile(
            user=user,
            first_name=data['profile']['first_name'].strip(),
            last_name=data['profile']['last_name'].strip(),
            joined_at=data['profile']['joined_at'],
            status=data['status'],
            status_changed_at=datetime.now())
        db.session.add(user_profile)

    db.session.add(user)
    db.session.commit()

    # response
    return jsonify({'user': UserSchema().dump(user)}), 201


@users.route('/user/<int:user_id>', methods=['GET'])
@users.route('/user/<string:username>', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_user(user_id=None, username=None):
    """Retrieves an existing user

    :param user_id: ID of user
    :type user_id: int
    :param username: Username of user
    :type username: str
    :returns: JSON string of the user's data; status code
    :rtype: (str, int)
    """

    # get user
    if user_id is not None:
        user = User.query.get(user_id)
    elif username is not None:
        try:
            user = User.query.filter(User.username == username).one()
        except NoResultFound:
            user = None
    if user is None:
        abort(404)

    # response
    return jsonify({'user': UserSchema().dump(user)}), 200


@users.route('/user/<int:user_id>', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def put_user(user_id):
    """Updates an existing user

    :param user_id: ID of user
    :type user_id: int
    :returns: JSON string of the user's data; status code
    :rtype: (str, int)
    """
    # pylint: disable=too-many-statements

    # get user
    user = User.query.get(user_id)
    if user is None:
        abort(404)

    # init vars
    errors = {}
    roles = []

    # pre-validate data
    if (request.json.get('username', None) and
            request.json.get('username') != user.username):
        user_query = User.query.filter(
            User.username == request.json.get('username')).first()
        if user_query:
            errors["username"] = ["Value must be unique."]

    if (request.json.get('email', None) and
            request.json.get('email') != user.email):
        temp_user = User(email=request.json.get('email'))
        user_query = User.query.filter(
            User.email_digest == temp_user.email_digest).first()
        if user_query:
            errors["email"] = ["Value must be unique."]

    if not request.json.get('roles', None):
        errors["roles"] = ["Missing data for required field."]
    else:
        for role_id in request.json.get('roles'):
            role = Role.query.get(role_id)
            if role is None:
                errors["roles"] = ["Invalid value."]
            else:
                roles.append(role.id)

    # validate data
    try:
        if request.json.get('password', None):
            data = UserSchema().load(request.json)
        else:
            data = UserSchema(exclude=('password',)).load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user
    user.username = data['username'].strip()
    user.email = data['email'].strip()
    user.is_verified = data['is_verified']

    if 'password' in data:
        user.password = data['password']

    user.roles[:] = []
    for role_id in roles:
        role = Role.query.get(role_id)
        user.roles.append(role)

    if user.status != data['status']:
        user.status = data['status']
        user.status_changed_at = datetime.now()

    # save user profile
    if 'profile' in data:
        user_profile = user.profile if user.profile else None
        if user_profile:
            user_profile.first_name = data['profile']['first_name'].strip()
            user_profile.last_name = data['profile']['last_name'].strip()
            user_profile.joined_at = data['profile']['joined_at']
            if user_profile.status != data['status']:
                user_profile.status = data['status']
                user_profile.status_changed_at = datetime.now()
        else:
            user_profile = UserProfile(
                user_id=user.id,
                first_name=data['profile']['first_name'].strip(),
                last_name=data['profile']['last_name'].strip(),
                joined_at=data['profile']['joined_at'],
                status=data['status'],
                status_changed_at=datetime.now())
            db.session.add(user_profile)

    db.session.commit()

    # response
    return jsonify({'user': UserSchema().dump(user)}), 200


@users.route('/user/<int:user_id>', methods=['DELETE'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def delete_user(user_id):
    """Deletes an existing user

    :param user_id: ID of user
    :type user_id: int
    :returns: Empty string; status code
    :rtype: (str, int)
    """

    # get user
    user = User.query.get(user_id)
    if user is None:
        abort(404)

    # delete user
    db.session.delete(user)
    db.session.commit()

    # response
    return '', 204
