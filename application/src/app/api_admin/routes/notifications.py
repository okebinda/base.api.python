from flask import Blueprint, jsonify, request, url_for

from app.models.Notification import Notification
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.NotificationSchema import NotificationSchema

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

    # initialize query
    notification_query = Notification.query

    # filter query based on URL parameters
    if request.args.get('user_id', None) is not None:
        notification_query = notification_query.filter(
            Notification.user_id == request.args.get('user_id'))
    if request.args.get('channel', None) is not None:
        notification_query = notification_query.filter(
            Notification.channel == request.args.get('channel'))
    if request.args.get('status', '').isnumeric():
        notification_query = notification_query.filter(
            Notification.status == int(request.args.get('status')))
    else:
        notification_query = notification_query.filter(
            Notification.status.in_((Notification.STATUS_ENABLED,
                                     Notification.STATUS_DISABLED,
                                     Notification.STATUS_PENDING)))

    # initialize order options dict
    order_options = {
        'id.asc': Notification.id.asc(),
        'id.desc': Notification.id.desc(),
        'sent_at.asc': Notification.sent_at.asc(),
        'sent_at.desc': Notification.sent_at.desc(),
    }

    # determine order
    if request.args.get('order_by') in order_options:
        order_by = order_options[request.args.get('order_by')]
    else:
        order_by = Notification.id.asc()

    # retrieve and return results
    notifications = notification_query.order_by(order_by).limit(limit).offset(
        (page - 1) * limit)
    if notifications.count():

        # prep initial output
        output = {
            'notifications': NotificationSchema(many=True).dump(
                notifications).data,
            'page': page,
            'limit': limit,
            'total': notification_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'notifications.get_notifications', page=page - 1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'notifications.get_notifications', page=page + 1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        return jsonify(output), 200
    else:
        return '', 204
