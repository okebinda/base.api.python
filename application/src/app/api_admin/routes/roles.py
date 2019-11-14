"""Roles controller"""

from flask import Blueprint, jsonify, abort, request
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from app import db
from app.models.Role import Role
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.RoleSchema import RoleSchema
from app.lib.routes.Pager import Pager

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
    """Retrieves a list of roles

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :param role_type: Type of role to filter by: `admin` | `user`
    :type role_type: str
    :returns: JSON string of list of roles; status code
    :rtype: (str, int)
    """

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
            'roles': RoleSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': role_query.count()
        }

        # add pagination URIs and return
        output.update(Pager.get_uris('roles.get_roles', page, limit,
                                     output['total'], request.args))
        return jsonify(output), 200
    else:
        return '', 204


@roles.route('/roles', methods=['POST'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def post_roles():
    """Creates a new role

    :returns: JSON string of the new role's data; status code
    :rtype: (str, int)
    """

    # init vars
    errors = {}

    # pre-validate data
    if request.json.get('name', None):
        role_query = Role.query.filter(
            Role.name == request.json.get('name')).first()
        if role_query:
            errors["name"] = ["Value must be unique."]

    # validate data
    try:
        data = RoleSchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

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
    return jsonify({'role': RoleSchema().dump(role)}), 201


@roles.route('/role/<int:role_id>', methods=['GET'])
@roles.route('/role/<string:name>', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_role(role_id=None, name=None):
    """Retrieves an existing role

    :param role_id: ID of role
    :type role_id: int
    :param name: Name of role
    :type name: str
    :returns: JSON string of the role's data; status code
    :rtype: (str, int)
    """

    # get role
    if role_id is not None:
        role = Role.query.get(role_id)
    elif name is not None:
        try:
            role = Role.query.filter(Role.name == name).one()
        except NoResultFound:
            role = None
    if role is None:
        abort(404)

    # response
    return jsonify({'role': RoleSchema().dump(role)}), 200


@roles.route('/role/<int:role_id>', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def put_role(role_id):
    """Updates an existing role

    :param role_id: ID of role
    :type role_id: int
    :returns: JSON string of the role's data; status code
    :rtype: (str, int)
    """

    # get role
    role = Role.query.get(role_id)
    if role is None:
        abort(404)

    # init vars
    errors = {}

    # pre-validate data
    if (request.json.get('name', None) and
            request.json.get('name') != role.name):
        role_query = Role.query.filter(
            Role.name == request.json.get('name')).first()
        if role_query:
            errors["name"] = ["Value must be unique."]

    # validate data
    try:
        data = RoleSchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

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
    return jsonify({'role': RoleSchema().dump(role)}), 200


@roles.route('/role/<int:role_id>', methods=['DELETE'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def delete_role(role_id):
    """Deletes an existing role

    :param role_id: ID of role
    :type role_id: int
    :returns: Empty string; status code
    :rtype: (str, int)
    """

    # get role
    role = Role.query.get(role_id)
    if role is None:
        abort(404)

    # delete role
    db.session.delete(role)
    db.session.commit()

    # response
    return '', 204
