"""
Admin controllers for the App Keys module.

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
from lib.schema.validate import unique
from .model import AppKey
from .schema_admin import AppKeyAdminSchema


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
            'created_at.asc': AppKey.created_at.asc(),
            'created_at.desc': AppKey.created_at.desc(),
            'updated_at.asc': AppKey.updated_at.asc(),
            'updated_at.desc': AppKey.updated_at.desc(),
        },
        request.args,
        Query.STATUS_FILTER_ADMIN)

    # retrieve and return results
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'app_keys': AppKeyAdminSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(Pager.get_uris('admin_app_keys.get_app_keys', page,
                                     limit, output['total'], request.args))
        return jsonify(output), 200

    return '', 204


def post_app_keys():
    """Creates a new application key

    :returns: JSON string of the new application key's data; status code
    :rtype: (str, int)
    """

    # pre-validate data
    errors = unique({}, AppKey, AppKey.key, request.json.get('key', None))

    errors = unique(errors, AppKey, AppKey.application,
                    request.json.get('application', None))

    # validate data
    try:
        data = AppKeyAdminSchema().load(request.json)
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
    return jsonify({'app_key': AppKeyAdminSchema().dump(app_key)}), 201


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
    return jsonify({'app_key': AppKeyAdminSchema().dump(app_key)}), 200


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

    # pre-validate data
    errors = unique({}, AppKey, AppKey.key, request.json.get('key', None),
                    update=app_key)

    # validate data
    try:
        data = AppKeyAdminSchema().load(request.json)
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
    return jsonify({'app_key': AppKeyAdminSchema().dump(app_key)}), 200


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
