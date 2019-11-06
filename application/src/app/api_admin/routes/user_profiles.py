"""User Profiles controller"""

from datetime import datetime

from flask import Blueprint, jsonify, abort, request, url_for
from marshmallow import ValidationError

from app import db
from app.models.UserProfile import UserProfile
from app.models.User import User
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.UserProfileSchema import UserProfileSchema

user_profiles = Blueprint('user_profiles', __name__)


@user_profiles.route("/user_profiles", methods=['GET'])
@user_profiles.route("/user_profiles/<int:page>", methods=['GET'])
@user_profiles.route("/user_profiles/<int:page>/<int(min=1, max=100):limit>",
                     methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_user_profiles(page=1, limit=10):
    """Retrieves a list of user profiles

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of user profiles; status code
    :rtype: (str, int)
    """

    # initialize query
    user_profile_query = UserProfile.query

    # filter query based on URL parameters
    if request.args.get('status', '').isnumeric():
        user_profile_query = user_profile_query.filter(
            UserProfile.status == int(request.args.get('status')))
    else:
        user_profile_query = user_profile_query.filter(
            UserProfile.status.in_((UserProfile.STATUS_ENABLED,
                                    UserProfile.STATUS_DISABLED,
                                    UserProfile.STATUS_PENDING)))

    # initialize order options dict
    order_options = {
        'id.asc': UserProfile.id.asc(),
        'id.desc': UserProfile.id.desc(),
        'user_id.asc': UserProfile.user_id.asc(),
        'user_id.desc': UserProfile.user_id.desc(),
        'joined_at.asc': UserProfile.joined_at.asc(),
        'joined_at.desc': UserProfile.joined_at.desc(),
    }

    # determine order
    if request.args.get('order_by') in order_options:
        order_by = order_options[request.args.get('order_by')]
    else:
        order_by = UserProfile.id.asc()

    # retrieve and return results
    results = user_profile_query.order_by(order_by).limit(limit).offset(
        (page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'user_profiles': UserProfileSchema(many=True).dump(
                results).data,
            'page': page,
            'limit': limit,
            'total': user_profile_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'user_profiles.get_user_profiles', page=page - 1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'user_profiles.get_user_profiles', page=page + 1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        return jsonify(output), 200
    else:
        return '', 204


@user_profiles.route('/user_profiles', methods=['POST'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def post_user_profiles():
    """Creates a new user profile

    :returns: JSON string of the new user profile's data; status code
    :rtype: (str, int)
    """

    # init vars
    errors = {}
    user = None

    if request.json.get('user_id', None):
        user = User.query.get(request.json.get('user_id'))
        if user is None:
            errors["user_id"] = ["Invalid value."]

    # validate data
    try:
        data, _ = UserProfileSchema(strict=True).load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user_profile
    user_profile = UserProfile(
        user=user,
        first_name=data['first_name'].strip(),
        last_name=data['last_name'].strip(),
        joined_at=data['joined_at'],
        status=data['status'],
        status_changed_at=datetime.now())
    db.session.add(user_profile)
    db.session.commit()

    # response
    return jsonify(
        {'user_profile': UserProfileSchema().dump(user_profile).data}), 201


@user_profiles.route('/user_profile/<int:user_profile_id>', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_user_profile(user_profile_id=None):
    """Retrieves an existing user profile

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
        {'user_profile': UserProfileSchema().dump(user_profile).data}), 200


@user_profiles.route('/user_profile/<int:user_profile_id>', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def put_user_profile(user_profile_id):
    """Updates an existing user profile

    :param user_profile_id: ID of user profile
    :type user_profile_id: int
    :returns: JSON string of the user profile's data; status code
    :rtype: (str, int)
    """

    # get user_profile
    user_profile = UserProfile.query.get(user_profile_id)
    if user_profile is None:
        abort(404)

    # init vars
    errors = {}
    user = None

    if request.json.get('user_id', None):
        user = User.query.get(request.json.get('user_id'))
        if user is None:
            errors["user_id"] = ["Invalid value."]

    # validate data
    try:
        data, _ = UserProfileSchema(strict=True).load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user_profile
    user_profile.user = user
    user_profile.first_name = data['first_name'].strip()
    user_profile.last_name = data['last_name'].strip()
    user_profile.joined_at = data['joined_at']
    if user_profile.status != data['status']:
        user_profile.status = data['status']
        user_profile.status_changed_at = datetime.now()
    db.session.commit()

    # response
    return jsonify(
        {'user_profile': UserProfileSchema().dump(user_profile).data}), 200


@user_profiles.route('/user_profile/<int:user_profile_id>', methods=['DELETE'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def delete_user_profile(user_profile_id):
    """Deletes an existing user profile

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
