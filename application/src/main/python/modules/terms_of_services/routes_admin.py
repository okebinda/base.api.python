"""
Admin controllers for the Terms of Services module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import datetime

from flask import jsonify, abort, request
from marshmallow import ValidationError

from init_dep import db
from lib.routes.pager import Pager
from lib.routes.query import Query
from .model import TermsOfService
from .schema_admin import TermsOfServiceSchema


def get_terms_of_services(page=1, limit=10):
    """Retrieves a list of terms of service.

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of terms of service; status code
    :rtype: (str, int)
    """

    # initialize query
    query = Query.make(
        TermsOfService,
        TermsOfService.id.asc(),
        {
            'id.asc': TermsOfService.id.asc(),
            'id.desc': TermsOfService.id.desc(),
            'publish_date.asc': TermsOfService.publish_date.asc(),
            'publish_date.desc': TermsOfService.publish_date.desc(),
            'version.asc': TermsOfService.version.asc(),
            'version.desc': TermsOfService.version.desc(),
        },
        request.args,
        Query.STATUS_FILTER_ADMIN)

    # retrieve and return results
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'terms_of_services': TermsOfServiceSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(
            Pager.get_uris('admin_terms_of_services.get_terms_of_services',
                           page,  limit, output['total'], request.args))
        return jsonify(output), 200

    return '', 204


def post_terms_of_services():
    """Creates a new terms of service.

    :returns: JSON string of the new terms of service's data; status code
    :rtype: (str, int)
    """

    # validate data
    try:
        data = TermsOfServiceSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # save terms of service
    tos = TermsOfService(
        text=data['text'],
        version=data['version'],
        publish_date=data['publish_date'],
        status=data['status'],
        status_changed_at=datetime.now())
    db.session.add(tos)
    db.session.commit()

    # response
    return jsonify({'terms_of_service': TermsOfServiceSchema().dump(tos)}), 201


def get_terms_of_service(terms_of_service_id=None):
    """Retrieves an existing terms of service.

    :param terms_of_service_id: ID of terms of service
    :type terms_of_service_id: int
    :returns: JSON string of the terms of service's data; status code
    :rtype: (str, int)
    """

    # get terms of service
    if terms_of_service_id is not None:
        tos = TermsOfService.query.get(terms_of_service_id)
    if tos is None:
        abort(404)

    # response
    return jsonify({'terms_of_service': TermsOfServiceSchema().dump(tos)}), 200


def put_terms_of_service(terms_of_service_id):
    """Updates an existing terms of service.

    :param terms_of_service_id: ID of terms of service
    :type terms_of_service_id: int
    :returns: JSON string of the terms of service's data; status code
    :rtype: (str, int)
    """

    # get terms of service
    tos = TermsOfService.query.get(terms_of_service_id)
    if tos is None:
        abort(404)

    # validate data
    try:
        data = TermsOfServiceSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # save terms of service
    tos.text = data['text']
    tos.version = data['version']
    tos.publish_date = data['publish_date']
    if tos.status != data['status']:
        tos.status = data['status']
        tos.status_changed_at = datetime.now()
    db.session.commit()

    # response
    return jsonify({'terms_of_service': TermsOfServiceSchema().dump(tos)}), 200


def delete_terms_of_service(terms_of_service_id):
    """Deletes an existing terms of service.

    :param terms_of_service_id: ID of terms of service
    :type terms_of_service_id: int
    :returns: Empty string; status code
    :rtype: (str, int)
    """

    # get terms of service
    tos = TermsOfService.query.get(terms_of_service_id)
    if tos is None:
        abort(404)

    # delete terms of service
    db.session.delete(tos)
    db.session.commit()

    # response
    return '', 204
