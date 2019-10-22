from datetime import datetime

from flask import Blueprint, jsonify, abort, request, url_for
from marshmallow import ValidationError

from app import db
from app.models.User import User
from app.models.Role import Role
from app.api_admin.authentication import auth, admin_permission, require_appkey, check_password_expiration
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
    users = user_query.order_by(order_by).limit(limit).offset((page-1)*limit)
    if users.count():

        # prep initial output
        output = {
            'users': UserSchema(many=True).dump(users).data,
            'page': page,
            'limit': limit,
            'total': user_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'users.get_users', page=page-1, limit=limit, _external=True,
                 order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'users.get_users', page=page+1, limit=limit, _external=True,
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

    # validate data
    try:
        data, _ = UserSchema(strict=True).load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))
    
    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user
    user = User(username=request.json.get('username').strip(),
                email=request.json.get('email').strip(),
                password=request.json.get('password'),
                is_verified=request.json.get('is_verified'),
                status=request.json.get('status'),
                status_changed_at=datetime.now())
    
    if request.json.get('roles', []) and len(request.json.get('roles')):
      for role_id in request.json.get('roles'):
          if role_id:
            role = Role.query.get(role_id)
            if role:
                user.roles.append(role)

    db.session.add(user)
    db.session.commit()

    # response
    return jsonify({'user': UserSchema().dump(user).data}), 201

@users.route('/user/<int:user_id>', methods=['GET'])
@users.route('/user/<string:username>', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_user(user_id=None, username=None):

    # get user
    if user_id is not None:
        user = User.query.get(user_id)
    elif username is not None:
        try:
            user = User.query.filter(User.username == username).one()
        except Exception:
            user = None
    if user is None:
        abort(404)

    # response
    return jsonify({'user': UserSchema().dump(user).data}), 200

@users.route('/user/<int:user_id>', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def put_user(user_id):

    # get user
    user = User.query.get(user_id)
    if user is None:
        abort(404)

    # init vars
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
        if request.json.get('password', None):
            data, _ = UserSchema(strict=True).load(request.json)
        else:
            data, _ = UserSchema(strict=True, exclude=('password',)).load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))
    
    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save user
    user.username = request.json.get('username', '').strip()
    user.email = request.json.get('email', '').strip()
    user.account_id = request.json.get('account_id', None)
    user.is_verified = request.json.get('is_verified', None)

    if request.json.get('password', None):
        user.password = request.json.get('password')

    user.roles[:] = []
    if request.json.get('roles') and isinstance(request.json.get('roles'), list):
        for role_id in request.json.get('roles'):
            role = Role.query.get(role_id)
            if role is not None:
                user.roles.append(role)
    
    if (user.status != request.json.get('status', None)):
        user.status = request.json.get('status')
        user.status_changed_at = datetime.now()

    db.session.commit()

    # response
    return jsonify({'user': UserSchema().dump(user).data}), 200

@users.route('/user/<int:user_id>', methods=['DELETE'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def delete_user(user_id):

    # get user
    user = User.query.get(user_id)
    if user is None:
        abort(404)

    # delete user
    db.session.delete(user)
    db.session.commit()

    # response
    return '', 204
