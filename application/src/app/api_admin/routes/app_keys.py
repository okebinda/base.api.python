from datetime import datetime

from flask import Blueprint, jsonify, abort, request, url_for
from marshmallow import ValidationError

from app import db
from app.models.AppKey import AppKey
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.AppKeySchema import AppKeySchema

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

    # initialize query
    app_key_query = AppKey.query

    # filter query based on URL parameters
    if request.args.get('status', '').isnumeric():
        app_key_query = app_key_query.filter(
            AppKey.status == int(request.args.get('status')))
    else:
        app_key_query = app_key_query.filter(
            AppKey.status.in_((AppKey.STATUS_ENABLED, AppKey.STATUS_DISABLED,
                               AppKey.STATUS_PENDING)))

    # initialize order options dict
    order_options = {
        'id.asc': AppKey.id.asc(),
        'id.desc': AppKey.id.desc(),
        'application.asc': AppKey.application.asc(),
        'application.desc': AppKey.application.desc(),
    }

    # determine order
    if request.args.get('order_by') in order_options:
        order_by = order_options[request.args.get('order_by')]
    else:
        order_by = AppKey.id.asc()

    # retrieve and return results
    results = app_key_query.order_by(order_by).limit(limit).offset(
        (page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'app_keys': AppKeySchema(many=True).dump(results).data,
            'page': page,
            'limit': limit,
            'total': app_key_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'app_keys.get_app_keys', page=page - 1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'app_keys.get_app_keys', page=page + 1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        return jsonify(output), 200
    else:
        return '', 204


@app_keys.route('/app_keys', methods=['POST'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def post_app_keys():

    # validate data
    try:
        data, _ = AppKeySchema(strict=True).load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # save app key
    app_key = AppKey(application=request.json.get('application'),
                     key=request.json.get('key'),
                     status=request.json.get('status'),
                     status_changed_at=datetime.now())
    db.session.add(app_key)
    db.session.commit()

    # response
    return jsonify({'app_key': AppKeySchema().dump(app_key).data}), 201


@app_keys.route('/app_key/<int:app_key_id>', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_app_key(app_key_id=None):

    # get app key
    if app_key_id is not None:
        app_key = AppKey.query.get(app_key_id)
    if app_key is None:
        abort(404)

    # response
    return jsonify({'app_key': AppKeySchema().dump(app_key).data}), 200


@app_keys.route('/app_key/<int:app_key_id>', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def put_app_key(app_key_id):

    # get app key
    app_key = AppKey.query.get(app_key_id)
    if app_key is None:
        abort(404)

    # validate data
    try:
        data, _ = AppKeySchema(strict=True).load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # save app key
    app_key.application = request.json.get('application', None)
    app_key.key = request.json.get('key', None)
    if app_key.status != request.json.get('status', None):
        app_key.status = request.json.get('status')
        app_key.status_changed_at = datetime.now()
    db.session.commit()

    # response
    return jsonify({'app_key': AppKeySchema().dump(app_key).data}), 200


@app_keys.route('/app_key/<int:app_key_id>', methods=['DELETE'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def delete_app_key(app_key_id):

    # get app key
    app_key = AppKey.query.get(app_key_id)
    if app_key is None:
        abort(404)

    # delete terms of service
    db.session.delete(app_key)
    db.session.commit()

    # response
    return '', 204
