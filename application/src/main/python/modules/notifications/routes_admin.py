"""
Admin controllers for the Notifications module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify, request

from lib.routes.pager import Pager
from lib.routes.query import Query
from .model import Notification
from .schema_admin import NotificationSchema


def get_notifications(page=1, limit=10):
    """Retrieves a list of notifications.

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of notifications; status code
    :rtype: (str, int)
    """

    # initialize query
    query = Query.make(
        Notification,
        Notification.id.asc(),
        {
            'id.asc': Notification.id.asc(),
            'id.desc': Notification.id.desc(),
            'sent_at.asc': Notification.sent_at.asc(),
            'sent_at.desc': Notification.sent_at.desc(),
        },
        request.args,
        Query.STATUS_FILTER_ADMIN)

    # filter query based on URL parameters
    if request.args.get('user_id', None) is not None:
        query = query.filter(
            Notification.user_id == request.args.get('user_id'))
    if request.args.get('channel', None) is not None:
        query = query.filter(
            Notification.channel == request.args.get('channel'))

    # retrieve and return results
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'notifications': NotificationSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(
            Pager.get_uris('admin_notifications.get_notifications', page,
                           limit, output['total'], request.args))
        return jsonify(output), 200

    return '', 204
