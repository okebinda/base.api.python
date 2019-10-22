from datetime import datetime

from flask import Blueprint, jsonify, abort, request, url_for
from marshmallow import ValidationError

from app import db
from app.models import UserProfile
from app.api_admin.authentication import auth, admin_permission, require_appkey, check_password_expiration
from app.api_admin.schema import UserProfileSchema

user_profiles = Blueprint('user_profiles', __name__)

@user_profiles.route("/user_profiles", methods=['GET'])
@user_profiles.route("/user_profiles/<int:page>", methods=['GET'])
@user_profiles.route("/user_profiles/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_user_profiles(page=1, limit=10):

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
    user_profiles = user_profile_query.order_by(order_by).limit(limit).offset((page-1)*limit)
    if user_profiles.count():

        # prep initial output
        output = {
            'user_profiles': UserProfileSchema(many=True).dump(user_profiles).data,
            'page': page,
            'limit': limit,
            'total': user_profile_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'user_profiles.get_user_profiles', page=page-1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'user_profiles.get_user_profiles', page=page+1, limit=limit,
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

    # validate data
    try:
        data, _ = UserProfileSchema(strict=True).load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # save user_profile
    user_profile = UserProfile(user_id=request.json.get('user_id'),
                               first_name=request.json.get('first_name', '').strip(),
                               last_name=request.json.get('last_name', '').strip(),
                               joined_at=request.json.get('joined_at'),
                               status=request.json.get('status'),
                               status_changed_at=datetime.now())
    db.session.add(user_profile)
    db.session.commit()

    # response
    return jsonify({'user_profile': UserProfileSchema().dump(user_profile).data}), 201

@user_profiles.route('/user_profile/<int:user_profile_id>', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_user_profile(user_profile_id=None):

    # get user_profile
    if user_profile_id is not None:
        user_profile = UserProfile.query.get(user_profile_id)
    if user_profile is None:
        abort(404)

    # response
    return jsonify({'user_profile': UserProfileSchema().dump(user_profile).data}), 200

@user_profiles.route('/user_profile/<int:user_profile_id>', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def put_user_profile(user_profile_id):

    # get user_profile
    user_profile = UserProfile.query.get(user_profile_id)
    if user_profile is None:
        abort(404)

    # validate data
    try:
        data, _ = UserProfileSchema(strict=True).load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # save user_profile
    user_profile.user_id = request.json.get('user_id', None)
    user_profile.first_name = request.json.get('first_name', '').strip()
    user_profile.last_name = request.json.get('last_name', '').strip()
    user_profile.joined_at = request.json.get('joined_at', None)
    if (user_profile.status != request.json.get('status', None)):
        user_profile.status = request.json.get('status')
        user_profile.status_changed_at = datetime.now()
    db.session.commit()

    # response
    return jsonify({'user_profile': UserProfileSchema().dump(user_profile).data}), 200

@user_profiles.route('/user_profile/<int:user_profile_id>', methods=['DELETE'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def delete_user_profile(user_profile_id):

    # get user_profile
    user_profile = UserProfile.query.get(user_profile_id)
    if user_profile is None:
        abort(404)

    # delete user_profile
    db.session.delete(user_profile)
    db.session.commit()

    # response
    return '', 204
