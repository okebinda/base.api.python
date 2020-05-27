"""
Admin controllers for the User Profiles module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member

from datetime import datetime

from flask import jsonify, abort, request
from marshmallow import ValidationError

from init_dep import db
from lib.routes.pager import Pager
from lib.routes.query import Query
from lib.schema.validate import exists
from modules.users.model import User
from .model import UserProfile
from .schema_admin import UserProfileSchema


def get_user_profiles(page=1, limit=10):
    """Retrieves a list of user profiles.

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of user profiles; status code
    :rtype: (str, int)
    """

    # initialize query
    query = Query.make(
        UserProfile,
        UserProfile.id.asc(),
        {
            'id.asc': UserProfile.id.asc(),
            'id.desc': UserProfile.id.desc(),
            'user_id.asc': UserProfile.user_id.asc(),
            'user_id.desc': UserProfile.user_id.desc(),
            'joined_at.asc': UserProfile.joined_at.asc(),
            'joined_at.desc': UserProfile.joined_at.desc(),
        },
        request.args,
        Query.STATUS_FILTER_ADMIN)

    # retrieve and return results
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'user_profiles': UserProfileSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(
            Pager.get_uris('admin_user_profiles.get_user_profiles', page,
                           limit, output['total'], request.args))
        return jsonify(output), 200

    return '', 204


def post_user_profiles():
    """Creates a new user profile.

    :returns: JSON string of the new user profile's data; status code
    :rtype: (str, int)
    """

    # pre-validate data
    errors, user = exists({}, User, 'user_id',
                          request.json.get('user_id', None))

    # validate data
    try:
        data = UserProfileSchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user_profile
    user_profile = UserProfile(
        user_id=user.id,
        first_name=data['first_name'].strip(),
        last_name=data['last_name'].strip(),
        joined_at=data['joined_at'],
        status=data['status'],
        status_changed_at=datetime.now())
    db.session.add(user_profile)
    db.session.commit()

    # response
    return jsonify(
        {'user_profile': UserProfileSchema().dump(user_profile)}), 201


def get_user_profile(user_profile_id=None):
    """Retrieves an existing user profile.

    :param user_profile_id: ID of user profile
    :type user_profile_id: int
    :returns: JSON string of the user profile's data; status code
    :rtype: (str, int)
    """

    # get user_profile
    if user_profile_id is not None:
        user_profile = UserProfile.query.get(user_profile_id)
    if user_profile is None:
        abort(404)

    # response
    return jsonify(
        {'user_profile': UserProfileSchema().dump(user_profile)}), 200


def put_user_profile(user_profile_id):
    """Updates an existing user profile.

    :param user_profile_id: ID of user profile
    :type user_profile_id: int
    :returns: JSON string of the user profile's data; status code
    :rtype: (str, int)
    """

    # get user_profile
    user_profile = UserProfile.query.get(user_profile_id)
    if user_profile is None:
        abort(404)

    # pre-validate data
    errors, user = exists({}, User, 'user_id',
                          request.json.get('user_id', None))

    # validate data
    try:
        data = UserProfileSchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user_profile
    user_profile.user_id = user.id
    user_profile.first_name = data['first_name'].strip()
    user_profile.last_name = data['last_name'].strip()
    user_profile.joined_at = data['joined_at']
    if user_profile.status != data['status']:
        user_profile.status = data['status']
        user_profile.status_changed_at = datetime.now()
    db.session.commit()

    # response
    return jsonify(
        {'user_profile': UserProfileSchema().dump(user_profile)}), 200


def delete_user_profile(user_profile_id):
    """Deletes an existing user profile.

    :param user_profile_id: ID of user profile
    :type user_profile_id: int
    :returns: Empty string; status code
    :rtype: (str, int)
    """

    # get user_profile
    user_profile = UserProfile.query.get(user_profile_id)
    if user_profile is None:
        abort(404)

    # delete user_profile
    db.session.delete(user_profile)
    db.session.commit()

    # response
    return '', 204
