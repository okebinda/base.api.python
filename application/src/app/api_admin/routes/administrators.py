"""Administrators controller"""

from datetime import datetime

from flask import Blueprint, jsonify, abort, request
from marshmallow import ValidationError

from app import db
from app.models.Administrator import Administrator
from app.models.Role import Role
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.AdministratorSchema import AdministratorSchema
from app.lib.routes.Pager import Pager
from app.lib.routes.Query import Query
from app.lib.schema.validate.unique import unique
from app.lib.schema.validate.unique_email import unique_email
from app.lib.schema.validate.exists import exists

administrators = Blueprint('administrators', __name__)


@administrators.route("/administrators", methods=['GET'])
@administrators.route("/administrators/<int:page>", methods=['GET'])
@administrators.route("/administrators/<int:page>/<int(min=1, max=100):limit>",
                      methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
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
    results = query.limit(limit).offset((page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'administrators': AdministratorSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(
            Pager.get_uris('administrators.get_administrators', page, limit,
                           output['total'], request.args))
        return jsonify(output), 200
    else:
        return '', 204


@administrators.route('/administrators', methods=['POST'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
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
        data = AdministratorSchema().load(request.json)
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

    for role_id in roles:
        role = Role.query.get(role_id)
        admin.roles.append(role)

    db.session.add(admin)
    db.session.commit()

    # response
    return jsonify(
        {'administrator': AdministratorSchema().dump(admin)}), 201


@administrators.route('/administrator/<int:administrator_id>', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
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
        {'administrator': AdministratorSchema().dump(administrator)}), 200


@administrators.route('/administrator/<int:administrator_id>', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
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
            data = AdministratorSchema().load(request.json)
        else:
            data = AdministratorSchema(
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
    for role_id in roles:
        role = Role.query.get(role_id)
        administrator.roles.append(role)

    if administrator.status != data['status']:
        administrator.status = data['status']
        administrator.status_changed_at = datetime.now()

    db.session.commit()

    # response
    return jsonify(
        {'administrator': AdministratorSchema().dump(administrator)}), 200


@administrators.route('/administrator/<int:administrator_id>',
                      methods=['DELETE'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
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
