from datetime import datetime

from flask import Blueprint, jsonify, abort, request, url_for
from marshmallow import ValidationError

from app import db
from app.models.TermsOfService import TermsOfService
from app.api_admin.authentication import auth, admin_permission, require_appkey, check_password_expiration
from app.api_admin.schema.TermsOfServiceSchema import TermsOfServiceSchema

terms_of_service = Blueprint('terms_of_service', __name__)


@terms_of_service.route("/terms_of_services", methods=['GET'])
@terms_of_service.route("/terms_of_services/<int:page>", methods=['GET'])
@terms_of_service.route("/terms_of_services/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_terms_of_services(page=1, limit=10):

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
    terms_of_services = terms_of_service_query.order_by(order_by).limit(limit).offset((page-1)*limit)
    if terms_of_services.count():

        # prep initial output
        output = {
            'terms_of_services': TermsOfServiceSchema(many=True).dump(terms_of_services).data,
            'page': page,
            'limit': limit,
            'total': terms_of_service_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'terms_of_service.get_terms_of_services', page=page-1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'terms_of_service.get_terms_of_services', page=page+1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        return jsonify(output), 200
    else:
        return '', 204


@terms_of_service.route('/terms_of_services', methods=['POST'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def post_terms_of_services():

    # validate data
    try:
        data, _ = TermsOfServiceSchema(strict=True).load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # save terms of service
    terms_of_service = TermsOfService(text=request.json.get('text'),
                                      version=request.json.get('version'),
                                      publish_date=request.json.get('publish_date'),
                                      status=request.json.get('status'),
                                      status_changed_at=datetime.now())
    db.session.add(terms_of_service)
    db.session.commit()

    # response
    return jsonify({'terms_of_service': TermsOfServiceSchema().dump(terms_of_service).data}), 201


@terms_of_service.route('/terms_of_service/<int:terms_of_service_id>', methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_terms_of_service(terms_of_service_id=None):

    # get terms of service
    if terms_of_service_id is not None:
        terms_of_service = TermsOfService.query.get(terms_of_service_id)
    if terms_of_service is None:
        abort(404)

    # response
    return jsonify({'terms_of_service': TermsOfServiceSchema().dump(terms_of_service).data}), 200


@terms_of_service.route('/terms_of_service/<int:terms_of_service_id>', methods=['PUT'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def put_terms_of_service(terms_of_service_id):

    # get terms of service
    terms_of_service = TermsOfService.query.get(terms_of_service_id)
    if terms_of_service is None:
        abort(404)

    # validate data
    try:
        data, _ = TermsOfServiceSchema(strict=True).load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # save terms of service
    terms_of_service.text = request.json.get('text', None)
    terms_of_service.version = request.json.get('version', None)
    terms_of_service.publish_date = request.json.get('publish_date', None)
    if (terms_of_service.status != request.json.get('status', None)):
        terms_of_service.status = request.json.get('status')
        terms_of_service.status_changed_at = datetime.now()
    db.session.commit()

    # response
    return jsonify({'terms_of_service': TermsOfServiceSchema().dump(terms_of_service).data}), 200


@terms_of_service.route('/terms_of_service/<int:terms_of_service_id>', methods=['DELETE'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def delete_terms_of_service(terms_of_service_id):

    # get terms of service
    terms_of_service = TermsOfService.query.get(terms_of_service_id)
    if terms_of_service is None:
        abort(404)

    # delete terms of service
    db.session.delete(terms_of_service)
    db.session.commit()

    # response
    return '', 204
