"""
Admin controllers for the Password Resets module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify, request

from lib.routes.pager import Pager
from lib.routes.query import Query
from .model import PasswordReset
from .schema_admin import PasswordResetSchema


def get_password_resets(page=1, limit=10):
    """Retrieves a list of password resets.

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of password resets; status code
    :rtype: (str, int)
    """

    # initialize query
    query = Query.make(
        PasswordReset,
        PasswordReset.id.asc(),
        {
            'id.asc': PasswordReset.id.asc(),
            'id.desc': PasswordReset.id.desc(),
            'requested_at.asc': PasswordReset.requested_at.asc(),
            'requested_at.desc': PasswordReset.requested_at.desc(),
        },
        request.args,
        Query.STATUS_FILTER_ADMIN)

    # filter query based on URL parameters
    if request.args.get('user_id', None) is not None:
        query = query.filter(
            PasswordReset.user_id == request.args.get('user_id'))

    # retrieve and return results
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'password_resets': PasswordResetSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(
            Pager.get_uris('admin_password_resets.get_password_resets', page,
                           limit, output['total'], request.args))
        return jsonify(output), 200

    return '', 204
