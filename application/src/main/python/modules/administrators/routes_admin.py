"""
Admin controllers for the Administrators module.

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
from lib.schema.validate import unique, unique_email, exists
from modules.roles.model import Role
from .model import Administrator
from .schema_admin import AdministratorAdminSchema


def get_administrators(page=1, limit=10):
    """Retrieves a list of administrators
    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of administrators; status code
    :rtype: (str, int)
    """

    # initialize query
    query = Query.make(
        Administrator,
        Administrator.id.asc(),
        {
            'id.asc': Administrator.id.asc(),
            'id.desc': Administrator.id.desc(),
            'username.asc': Administrator.username.asc(),
            'username.desc': Administrator.username.desc(),
            'joined_at.asc': Administrator.joined_at.asc(),
            'joined_at.desc': Administrator.joined_at.desc(),
        },
        request.args,
        Query.STATUS_FILTER_ADMIN)

    # filter by role
    if request.args.get('role', '').isnumeric():
        query = query.filter(Administrator.roles.any(
            Role.id == int(request.args.get('role'))))

    # retrieve and return results
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'administrators': AdministratorAdminSchema(
                many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(
            Pager.get_uris('admin_administrators.get_administrators', page,
                           limit, output['total'], request.args))
        return jsonify(output), 200

    return '', 204


def post_administrator():
    """Creates a new administrator
    :returns: JSON string of the new administrator's data; status code
    :rtype: (str, int)
    """

    # pre-validate data
    errors = unique({}, Administrator, Administrator.username,
                    request.json.get('username', None))

    errors = unique_email(errors, Administrator, Administrator.email,
                          request.json.get('email', None))

    errors, roles = exists(errors, Role, 'roles',
                           request.json.get('roles', []))

    # validate data
    try:
        data = AdministratorAdminSchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save admin
    admin = Administrator(username=data['username'],
                          email=data['email'],
                          first_name=data['first_name'],
                          last_name=data['last_name'],
                          password=data['password'],
                          joined_at=data['joined_at'],
                          status=data['status'],
                          status_changed_at=datetime.now())

    for role in roles:
        admin.roles.append(role)

    db.session.add(admin)
    db.session.commit()

    # response
    return jsonify(
        {'administrator': AdministratorAdminSchema().dump(admin)}), 201


def get_administrator(administrator_id=None):
    """Retrieves an existing administrator
    :param administrator_id: ID of administrator
    :type administrator_id: int
    :returns: JSON string of the administrator's data; status code
    :rtype: (str, int)
    """

    # get administrator
    if administrator_id is not None:
        administrator = Administrator.query.get(administrator_id)
    if administrator is None:
        abort(404)

    # response
    return jsonify(
        {'administrator': AdministratorAdminSchema().dump(administrator)}), 200


def put_administrator(administrator_id):
    """Updates an existing administrator
    :param administrator_id: ID of administrator
    :type administrator_id: int
    :returns: JSON string of the administrator's data; status code
    :rtype: (str, int)
    """

    # get administrator
    administrator = Administrator.query.get(administrator_id)
    if administrator is None:
        abort(404)

    # pre-validate data
    errors = unique({}, Administrator, Administrator.username,
                    request.json.get('username', None), update=administrator)

    errors = unique_email(errors, Administrator, Administrator.email,
                          request.json.get('email', None),
                          update=administrator)

    errors, roles = exists(errors, Role, 'roles',
                           request.json.get('roles', []))

    # validate data
    try:
        if request.json.get('password', None):
            data = AdministratorAdminSchema().load(request.json)
        else:
            data = AdministratorAdminSchema(
                exclude=('password',)).load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save administrator
    administrator.username = data['username']
    administrator.email = data['email']
    administrator.first_name = data['first_name']
    administrator.last_name = data['last_name']
    administrator.joined_at = data['joined_at']

    if 'password' in data:
        administrator.password = data['password']

    administrator.roles[:] = []
    for role in roles:
        administrator.roles.append(role)

    if administrator.status != data['status']:
        administrator.status = data['status']
        administrator.status_changed_at = datetime.now()

    db.session.commit()

    # response
    return jsonify(
        {'administrator': AdministratorAdminSchema().dump(administrator)}), 200


def delete_administrator(administrator_id):
    """Deletes an existing administrator
    :param administrator_id: ID of administrator
    :type administrator_id: int
    :returns: Empty string; status code
    :rtype: (str, int)
    """

    # get administrator
    administrator = Administrator.query.get(administrator_id)
    if administrator is None:
        abort(404)

    # delete administrator
    db.session.delete(administrator)
    db.session.commit()

    # response
    return '', 204
