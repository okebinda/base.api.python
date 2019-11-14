"""Notifications controller"""

from flask import Blueprint, jsonify, request

from app.models.Notification import Notification
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.NotificationSchema import NotificationSchema
from app.lib.routes.Pager import Pager
from app.lib.routes.Query import Query

notifications = Blueprint('notifications', __name__)


@notifications.route("/notifications", methods=['GET'])
@notifications.route("/notifications/<int:page>", methods=['GET'])
@notifications.route("/notifications/<int:page>/<int(min=1, max=100):limit>",
                     methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_notifications(page=1, limit=10):
    """Retrieves a list of notifications

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
    results = query.limit(limit).offset((page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'notifications': NotificationSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(
            Pager.get_uris('notifications.get_notifications', page, limit,
                           output['total'], request.args))
        return jsonify(output), 200
    else:
        return '', 204
