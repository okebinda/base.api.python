"""
Public controllers for the Terms of Services module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member

from flask import jsonify

from .model import TermsOfService
from .schema_public import TermsOfServiceSchema


def get_terms_of_service():
    """Retrieves the most recent Terms of Service.

    :returns: JSON string of the Terms of Service; status code
    :rtype: (str, int)
    """

    # initialize query
    terms_of_service_query = TermsOfService.query.filter(
        TermsOfService.status == TermsOfService.STATUS_ENABLED)

    # determine order
    order_by = TermsOfService.version.desc()

    # retrieve and return results
    terms_of_services = list(
        terms_of_service_query.order_by(order_by).limit(1))
    if len(terms_of_services) > 0:
        return jsonify(
            {'terms_of_service': TermsOfServiceSchema().dump(
                terms_of_services[0])}), 200

    return '', 204
