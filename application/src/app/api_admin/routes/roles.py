from flask import Blueprint, jsonify, abort, request, url_for
from marshmallow import ValidationError

from app import db
from app.models.Role import Role
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.RoleSchema import RoleSchema

roles = Blueprint('roles', __name__)


@roles.route("/roles", methods=['GET'])
@roles.route("/roles/<int:page>", methods=['GET'])
@roles.route("/roles/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])
@roles.route("/roles/<string:role_type>", methods=['GET'])
@roles.route("/roles/<string:role_type>/<int:page>", methods=['GET'])
@roles.route(
    "/roles/<string:role_type>/<int:page>/<int(min=1, max=100):limit>",
    methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_roles(page=1, limit=10, role_type=None):

    # initialize query
    role_query = Role.query

    # filter query based on URL parameters
    if role_type in ['admin', 'user']:
        role_query = role_query.filter(
            Role.is_admin_role == bool(role_type == 'admin'))

    # initialize order options dict
    order_options = {
        'id.asc': Role.id.asc(),
        'id.desc': Role.id.desc(),
        'name.asc': Role.name.asc(),
        'name.desc': Role.name.desc(),
    }

    # determine order
    if request.args.get('order_by') in order_options:
        order_by = order_options[request.args.get('order_by')]
    else:
        order_by = Role.id.asc()

    # retrieve and return results
    results = role_query.order_by(order_by).limit(limit).offset(
        (page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'roles': RoleSchema(many=True).dump(results).data,
            'page': page,
            'limit': limit,
            'total': role_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'roles.get_roles', page=page - 1, limit=limit, _external=True,
                order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'roles.get_roles', page=page + 1, limit=limit, _external=True,
                order_by=request.args.get('order_by', None))
        return jsonify(output), 200
    else:
        return '', 204


@roles.route('/roles', methods=['POST'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def post_roles():

    # validate data
    try:
        data, _ = RoleSchema(strict=True).load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # save role
    role = Role(
        name=data['name'],
        is_admin_role=data['is_admin_role'],
        priority=data['priority'],
        login_lockout_policy=data['login_lockout_policy'],
        login_max_attempts=data['login_max_attempts'],
        login_timeframe=data['login_timeframe'],
        login_ban_time=data['login_ban_time'],
        login_ban_by_ip=data['login_ban_by_ip'],
        password_policy=data['password_policy'],
        password_reuse_history=data['password_reuse_history'],
        password_reset_days=data['password_reset_days'])
    db.session.add(role)
    db.session.commit()

    # response
    return jsonify({'role': RoleSchema().dump(role).data}), 201


@roles.route('/role/<int:role_id>', methods=['GET'])
@roles.route('/role/<string:name>', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_role(role_id=None, name=None):

    # get role
    if role_id is not None:
        role = Role.query.get(role_id)
    elif name is not None:
        try:
            role = Role.query.filter(Role.name == name).one()
        except Exception:
            role = None
    if role is None:
        abort(404)

    # response
    return jsonify({'role': RoleSchema().dump(role).data}), 200


@roles.route('/role/<int:role_id>', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def put_role(role_id):

    # get role
    role = Role.query.get(role_id)
    if role is None:
        abort(404)

    # validate data
    try:
        data, _ = RoleSchema(strict=True).load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # save role
    role.name = data['name']
    role.is_admin_role = data['is_admin_role']
    role.priority = data['priority']
    role.login_lockout_policy = data['login_lockout_policy']
    role.login_max_attempts = data['login_max_attempts']
    role.login_timeframe = data['login_timeframe']
    role.login_ban_time = data['login_ban_time']
    role.login_ban_by_ip = data['login_ban_by_ip']
    role.password_policy = data['password_policy']
    role.password_reuse_history = data['password_reuse_history']
    role.password_reset_days = data['password_reset_days']
    db.session.commit()

    # response
    return jsonify({'role': RoleSchema().dump(role).data}), 200


@roles.route('/role/<int:role_id>', methods=['DELETE'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def delete_role(role_id):

    # get role
    role = Role.query.get(role_id)
    if role is None:
        abort(404)

    # delete role
    db.session.delete(role)
    db.session.commit()

    # response
    return '', 204
