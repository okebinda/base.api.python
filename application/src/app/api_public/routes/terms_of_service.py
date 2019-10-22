from flask import Blueprint, jsonify

from app.models.TermsOfService import TermsOfService
from app.api_public.authentication import require_appkey
from app.api_public.schema.TermsOfServiceSchema import TermsOfServiceSchema

terms_of_service = Blueprint('terms_of_service', __name__)


@terms_of_service.route("/terms_of_service/current", methods=['GET'])
@require_appkey
def get_terms_of_service():

    # initialize query
    terms_of_service_query = TermsOfService.query.filter(
        TermsOfService.status == TermsOfService.STATUS_ENABLED)

    # determine order
    order_by = TermsOfService.version.desc()

    # retrieve and return results
    terms_of_services = terms_of_service_query.order_by(order_by).limit(1)
    if terms_of_services.count():
        return jsonify({'terms_of_service': TermsOfServiceSchema().dump(terms_of_services[0]).data}), 200
    else:
        return '', 204
