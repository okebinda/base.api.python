"""
Admin controllers for the Users module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member

from datetime import datetime

from flask import jsonify, abort, request
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from init_dep import db
from lib.routes.pager import Pager
from lib.routes.query import Query
from lib.schema.validate import unique, unique_email, exists
from modules.roles.model import Role
from modules.user_profiles.model import UserProfile
from .model import User
from .schema_admin import UserAdminSchema


def get_users(page=1, limit=10):
    """Retrieves a list of users.

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of users; status code
    :rtype: (str, int)
    """

    # initialize query
    query = Query.make(
        User,
        User.id.asc(),
        {
            'id.asc': User.id.asc(),
            'id.desc': User.id.desc(),
            'username.asc': User.username.asc(),
            'username.desc': User.username.desc(),
            'created_at.asc': User.created_at.asc(),
            'created_at.desc': User.created_at.desc(),
            'updated_at.asc': User.updated_at.asc(),
            'updated_at.desc': User.updated_at.desc(),
        },
        request.args,
        Query.STATUS_FILTER_ADMIN)

    # filter query based on URL parameters
    if request.args.get('role', '').isnumeric():
        query = query.filter(
            User.roles.any(Role.id == int(request.args.get('role'))))
    if request.args.get('username', None) is not None:
        query = query.filter(
            User.username.ilike('%' + request.args.get('username') + '%'))
    if request.args.get('email', None) is not None:
        temp_user = User(email=request.args.get('email'))
        query = query.filter(
            User.email_digest == temp_user.email_digest)

    # retrieve and return results
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'users': UserAdminSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(Pager.get_uris('admin_users.get_users', page, limit,
                                     output['total'], request.args))
        return jsonify(output), 200

    return '', 204


def post_user():
    """Creates a new user.

    :returns: JSON string of the new user's data; status code
    :rtype: (str, int)
    """

    # pre-validate data
    errors = unique({}, User, User.username,
                    request.json.get('username', None))

    errors = unique_email(errors, User, User.email,
                          request.json.get('email', None))

    errors, roles = exists(errors, Role, 'roles',
                           request.json.get('roles', []))

    # validate data
    try:
        data = UserAdminSchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user
    user = User(username=data['username'].lower().strip(),
                email=data['email'].lower().strip(),
                password=data['password'],
                is_verified=data['is_verified'],
                status=data['status'],
                status_changed_at=datetime.now())

    for role in roles:
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
    return jsonify({'user': UserAdminSchema().dump(user)}), 201


def get_user(user_id=None, username=None):
    """Retrieves an existing user.

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
    return jsonify({'user': UserAdminSchema().dump(user)}), 200


def put_user(user_id):
    """Updates an existing user.

    :param user_id: ID of user
    :type user_id: int
    :returns: JSON string of the user's data; status code
    :rtype: (str, int)
    """

    # get user
    user = User.query.get(user_id)
    if user is None:
        abort(404)

    # pre-validate data
    errors = unique({}, User, User.username,
                    request.json.get('username', None), update=user)

    errors = unique_email(errors, User, User.email,
                          request.json.get('email', None), update=user)

    errors, roles = exists(errors, Role, 'roles',
                           request.json.get('roles', []))

    # validate data
    try:
        if request.json.get('password', None):
            data = UserAdminSchema().load(request.json)
        else:
            data = UserAdminSchema(exclude=('password',)).load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user
    user.username = data['username'].lower().strip()
    user.email = data['email'].lower().strip()
    user.is_verified = data['is_verified']

    if 'password' in data:
        user.password = data['password']

    user.roles[:] = []
    for role in roles:
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
            user.profile = user_profile

    db.session.commit()

    # response
    return jsonify({'user': UserAdminSchema().dump(user)}), 200


def delete_user(user_id):
    """Deletes an existing user.

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
