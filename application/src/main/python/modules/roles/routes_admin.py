"""
Admin controllers for the Roles module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member

from flask import jsonify, abort, request
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from init_dep import db
from lib.routes.pager import Pager
from lib.routes.query import Query
from lib.schema.validate import unique
from .model import Role
from .schema_admin import RoleAdminSchema


def get_roles(page=1, limit=10, role_type=None):
    """Retrieves a list of roles.

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
    query = Query.make(
        Role,
        Role.id.asc(),
        {
            'id.asc': Role.id.asc(),
            'id.desc': Role.id.desc(),
            'name.asc': Role.name.asc(),
            'name.desc': Role.name.desc(),
        },
        request.args,
        Query.STATUS_FILTER_NONE)

    # filter query based on URL parameters
    if role_type in ['admin', 'user']:
        query = query.filter(
            Role.is_admin_role == bool(role_type == 'admin'))

    # retrieve and return results
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'roles': RoleAdminSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(Pager.get_uris('admin_roles.get_roles', page, limit,
                                     output['total'], request.args,
                                     role_type=role_type))
        return jsonify(output), 200

    return '', 204


def post_roles():
    """Creates a new role.

    :returns: JSON string of the new role's data; status code
    :rtype: (str, int)
    """

    # pre-validate data
    errors = {}
    if isinstance(request.json.get('name', None), str):
        errors = unique(errors, Role, Role.name, request.json.get('name'))

    # validate data
    try:
        data = RoleAdminSchema().load(request.json)
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
    return jsonify({'role': RoleAdminSchema().dump(role)}), 201


def get_role(role_id=None, name=None):
    """Retrieves an existing role.

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
    return jsonify({'role': RoleAdminSchema().dump(role)}), 200


def put_role(role_id):
    """Updates an existing role.

    :param role_id: ID of role
    :type role_id: int
    :returns: JSON string of the role's data; status code
    :rtype: (str, int)
    """

    # get role
    role = Role.query.get(role_id)
    if role is None:
        abort(404)

    # pre-validate data
    errors = {}
    if isinstance(request.json.get('name', None), str):
        errors = unique(errors, Role, Role.name, request.json.get('name'),
                        update=role)

    # validate data
    try:
        data = RoleAdminSchema().load(request.json)
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
    return jsonify({'role': RoleAdminSchema().dump(role)}), 200


def delete_role(role_id):
    """Deletes an existing role.

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
