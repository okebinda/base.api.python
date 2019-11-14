"""Terms of Services controller"""

from datetime import datetime

from flask import Blueprint, jsonify, abort, request
from marshmallow import ValidationError

from app import db
from app.models.TermsOfService import TermsOfService
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.TermsOfServiceSchema import TermsOfServiceSchema
from app.lib.routes.Pager import Pager

terms_of_service = Blueprint('terms_of_service', __name__)


@terms_of_service.route("/terms_of_services", methods=['GET'])
@terms_of_service.route("/terms_of_services/<int:page>", methods=['GET'])
@terms_of_service.route(
    "/terms_of_services/<int:page>/<int(min=1, max=100):limit>",
    methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_terms_of_services(page=1, limit=10):
    """Retrieves a list of terms of service

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of terms of service; status code
    :rtype: (str, int)
    """

    # initialize query
    terms_of_service_query = TermsOfService.query

    # filter query based on URL parameters
    if request.args.get('status', '').isnumeric():
        terms_of_service_query = terms_of_service_query.filter(
            TermsOfService.status == int(request.args.get('status')))
    else:
        terms_of_service_query = terms_of_service_query.filter(
            TermsOfService.status.in_((TermsOfService.STATUS_ENABLED,
                                       TermsOfService.STATUS_DISABLED,
                                       TermsOfService.STATUS_PENDING)))

    # initialize order options dict
    order_options = {
        'id.asc': TermsOfService.id.asc(),
        'id.desc': TermsOfService.id.desc(),
        'publish_date.asc': TermsOfService.publish_date.asc(),
        'publish_date.desc': TermsOfService.publish_date.desc(),
        'version.asc': TermsOfService.version.asc(),
        'version.desc': TermsOfService.version.desc(),
    }

    # determine order
    if request.args.get('order_by') in order_options:
        order_by = order_options[request.args.get('order_by')]
    else:
        order_by = TermsOfService.id.asc()

    # retrieve and return results
    results = terms_of_service_query.order_by(order_by).limit(
        limit).offset((page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'terms_of_services': TermsOfServiceSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': terms_of_service_query.count()
        }

        # add pagination URIs and return
        Pager.update(output, 'terms_of_service.get_terms_of_services', page,
                     limit, request.args)
        return jsonify(output), 200
    else:
        return '', 204


@terms_of_service.route('/terms_of_services', methods=['POST'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def post_terms_of_services():
    """Creates a new terms of service

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


@terms_of_service.route('/terms_of_service/<int:terms_of_service_id>',
                        methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_terms_of_service(terms_of_service_id=None):
    """Retrieves an existing terms of service

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


@terms_of_service.route('/terms_of_service/<int:terms_of_service_id>',
                        methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def put_terms_of_service(terms_of_service_id):
    """Updates an existing terms of service

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


@terms_of_service.route('/terms_of_service/<int:terms_of_service_id>',
                        methods=['DELETE'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def delete_terms_of_service(terms_of_service_id):
    """Deletes an existing terms of service

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
