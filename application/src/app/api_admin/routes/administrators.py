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
    administrator_query = Administrator.query

    # filter query based on URL parameters
    if request.args.get('status', '').isnumeric():
        administrator_query = administrator_query.filter(
            Administrator.status == int(request.args.get('status')))
    else:
        administrator_query = administrator_query.filter(
            Administrator.status.in_((Administrator.STATUS_ENABLED,
                                      Administrator.STATUS_DISABLED,
                                      Administrator.STATUS_PENDING)))

    if request.args.get('role', '').isnumeric():
        administrator_query = administrator_query.filter(
            Administrator.roles.any(Role.id == int(request.args.get('role'))))

    # initialize order options dict
    order_options = {
        'id.asc': Administrator.id.asc(),
        'id.desc': Administrator.id.desc(),
        'username.asc': Administrator.username.asc(),
        'username.desc': Administrator.username.desc(),
        'joined_at.asc': Administrator.joined_at.asc(),
        'joined_at.desc': Administrator.joined_at.desc(),
    }

    # determine order
    if request.args.get('order_by') in order_options:
        order_by = order_options[request.args.get('order_by')]
    else:
        order_by = Administrator.id.asc()

    # retrieve and return results
    results = administrator_query.order_by(order_by).limit(
        limit).offset((page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'administrators': AdministratorSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': administrator_query.count()
        }

        # add pagination URIs and return
        Pager.update(output, 'administrators.get_administrators', page, limit,
                     request.args)
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

    # init vars
    errors = {}
    roles = []

    # pre-validate data
    if request.json.get('username', None):
        administrator_query = Administrator.query.filter(
            Administrator.username == request.json.get('username')).first()
        if administrator_query:
            errors["username"] = ["Value must be unique."]

    if request.json.get('email', None):
        temp_admin = Administrator(email=request.json.get('email'))
        administrator_query = Administrator.query.filter(
            Administrator.email_digest == temp_admin.email_digest).first()
        if administrator_query:
            errors["email"] = ["Value must be unique."]

    if not request.json.get('roles', None):
        errors["roles"] = ["Missing data for required field."]
    else:
        for role_id in request.json.get('roles'):
            role = Role.query.get(role_id)
            if role is None:
                errors["roles"] = ["Invalid value."]
            else:
                roles.append(role.id)

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

    # init vars
    errors = {}
    roles = []

    # pre-validate data
    if (request.json.get('username', None) and
            request.json.get('username') != administrator.username):
        administrator_query = Administrator.query.filter(
            Administrator.username == request.json.get('username')).first()
        if administrator_query:
            errors["username"] = ["Value must be unique."]

    if (request.json.get('email', None) and
            request.json.get('email') != administrator.email):
        temp_admin = Administrator(email=request.json.get('email'))
        administrator_query = Administrator.query.filter(
            Administrator.email_digest == temp_admin.email_digest).first()
        if administrator_query:
            errors["email"] = ["Value must be unique."]

    if not request.json.get('roles', None):
        errors["roles"] = ["Missing data for required field."]
    else:
        for role_id in request.json.get('roles'):
            role = Role.query.get(role_id)
            if role is None:
                errors["roles"] = ["Invalid value."]
            else:
                roles.append(role.id)

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
