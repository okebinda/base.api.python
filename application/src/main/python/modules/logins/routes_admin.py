"""
Admin controllers for the Logins module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify, request

from lib.routes.pager import Pager
from lib.routes.query import Query
from .model import Login
from .schema_admin import LoginSchema


def get_logins(page=1, limit=25):
    """Retrieves a list of logins.

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of logins; status code
    :rtype: (str, int)
    """

    # initialize query
    query = Query.make(
        Login,
        Login.id.asc(),
        {
            'id.asc': Login.id.asc(),
            'id.desc': Login.id.desc(),
            'attempt_date.asc': Login.attempt_date.asc(),
            'attempt_date.desc': Login.attempt_date.desc(),
        },
        request.args,
        Query.STATUS_FILTER_NONE)

    # filter query based on URL parameters
    if request.args.get('user_id', None) is not None:
        query = query.filter(
            Login.user_id == request.args.get('user_id'))
    if request.args.get('username', None) is not None:
        query = query.filter(
            Login.username == request.args.get('username'))
    if request.args.get('ip_address', None) is not None:
        query = query.filter(
            Login.ip_address == request.args.get('ip_address'))
    if request.args.get('api', None) is not None:
        query = query.filter(
            Login.api == request.args.get('api'))

    # retrieve and return results
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'logins': LoginSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(Pager.get_uris('admin_logins.get_logins', page, limit,
                                     output['total'], request.args))
        return jsonify(output), 200

    return '', 204
