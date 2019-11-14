"""Application Keys controller"""

from datetime import datetime

from flask import Blueprint, jsonify, abort, request
from marshmallow import ValidationError

from app import db
from app.models.AppKey import AppKey
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.AppKeySchema import AppKeySchema
from app.lib.routes.Pager import Pager
from app.lib.routes.Query import Query

app_keys = Blueprint('app_keys', __name__)


@app_keys.route("/app_keys", methods=['GET'])
@app_keys.route("/app_keys/<int:page>", methods=['GET'])
@app_keys.route("/app_keys/<int:page>/<int(min=1, max=100):limit>",
                methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_app_keys(page=1, limit=10):
    """Retrieves a list of application keys

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of application keys; status code
    :rtype: (str, int)
    """

    # initialize query
    query = Query.make(
        AppKey,
        AppKey.id.asc(),
        {
            'id.asc': AppKey.id.asc(),
            'id.desc': AppKey.id.desc(),
            'application.asc': AppKey.application.asc(),
            'application.desc': AppKey.application.desc(),
        },
        request.args,
        Query.STATUS_FILTER_ADMIN)

    # retrieve and return results
    results = query.limit(limit).offset((page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'app_keys': AppKeySchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(Pager.get_uris('app_keys.get_app_keys', page, limit,
                                     output['total'], request.args))
        return jsonify(output), 200
    else:
        return '', 204


@app_keys.route('/app_keys', methods=['POST'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def post_app_keys():
    """Creates a new application key

    :returns: JSON string of the new application key's data; status code
    :rtype: (str, int)
    """

    # init vars
    errors = {}

    # pre-validate data
    if request.json.get('key', None):
        app_key_query = AppKey.query.filter(
            AppKey.key == request.json.get('key')).first()
        if app_key_query:
            errors["key"] = ["Value must be unique."]

    # validate data
    try:
        data = AppKeySchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save app key
    app_key = AppKey(application=data['application'],
                     key=data['key'],
                     status=data['status'],
                     status_changed_at=datetime.now())
    db.session.add(app_key)
    db.session.commit()

    # response
    return jsonify({'app_key': AppKeySchema().dump(app_key)}), 201


@app_keys.route('/app_key/<int:app_key_id>', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_app_key(app_key_id=None):
    """Retrieves an existing application key

    :param app_key_id: ID of application key
    :type app_key_id: int
    :returns: JSON string of the application key's data; status code
    :rtype: (str, int)
    """

    # get app key
    if app_key_id is not None:
        app_key = AppKey.query.get(app_key_id)
    if app_key is None:
        abort(404)

    # response
    return jsonify({'app_key': AppKeySchema().dump(app_key)}), 200


@app_keys.route('/app_key/<int:app_key_id>', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def put_app_key(app_key_id):
    """Updates an existing application key

    :param app_key_id: ID of application key
    :type app_key_id: int
    :returns: JSON string of the application key's data; status code
    :rtype: (str, int)
    """

    # get app key
    app_key = AppKey.query.get(app_key_id)
    if app_key is None:
        abort(404)

    # init vars
    errors = {}

    # pre-validate data
    if (request.json.get('key', None) and
            request.json.get('key') != app_key.key):
        app_key_query = AppKey.query.filter(
            AppKey.key == request.json.get('key')).first()
        if app_key_query:
            errors["key"] = ["Value must be unique."]

    # validate data
    try:
        data = AppKeySchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save app key
    app_key.application = data['application']
    app_key.key = data['key']
    if app_key.status != data['status']:
        app_key.status = data['status']
        app_key.status_changed_at = datetime.now()
    db.session.commit()

    # response
    return jsonify({'app_key': AppKeySchema().dump(app_key)}), 200


@app_keys.route('/app_key/<int:app_key_id>', methods=['DELETE'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def delete_app_key(app_key_id):
    """Deletes an existing application key

    :param app_key_id: ID of application key
    :type app_key_id: int
    :returns: Empty string; status code
    :rtype: (str, int)
    """

    # get app key
    app_key = AppKey.query.get(app_key_id)
    if app_key is None:
        abort(404)

    # delete terms of service
    if request.args.get('permanent', None):
        db.session.delete(app_key)

    # set delete status
    else:
        app_key.status = AppKey.STATUS_DELETED
        app_key.status_changed_at = datetime.now()

    db.session.commit()

    # response
    return '', 204
