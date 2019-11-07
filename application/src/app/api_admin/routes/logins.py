"""Logins controller"""

from flask import Blueprint, jsonify, request, url_for

from app.models.Login import Login
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.LoginSchema import LoginSchema

logins = Blueprint('logins', __name__)


@logins.route("/logins", methods=['GET'])
@logins.route("/logins/<int:page>", methods=['GET'])
@logins.route("/logins/<int:page>/<int(min=1, max=100):limit>",
              methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_logins(page=1, limit=25):
    """Retrieves a list of logins

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of logins; status code
    :rtype: (str, int)
    """

    # initialize query
    login_query = Login.query

    # filter query based on URL parameters
    if request.args.get('user_id', None) is not None:
        login_query = login_query.filter(
            Login.user_id == request.args.get('user_id'))
    if request.args.get('username', None) is not None:
        login_query = login_query.filter(
            Login.username == request.args.get('username'))
    if request.args.get('ip_address', None) is not None:
        login_query = login_query.filter(
            Login.ip_address == request.args.get('ip_address'))
    if request.args.get('api', None) is not None:
        login_query = login_query.filter(
            Login.api == request.args.get('api'))

    # initialize order options dict
    order_options = {
        'id.asc': Login.id.asc(),
        'id.desc': Login.id.desc(),
        'attempt_date.asc': Login.attempt_date.asc(),
        'attempt_date.desc': Login.attempt_date.desc(),
    }

    # determine order
    if request.args.get('order_by') in order_options:
        order_by = order_options[request.args.get('order_by')]
    else:
        order_by = Login.id.asc()

    # retrieve and return results
    results = login_query.order_by(order_by).limit(limit).offset(
        (page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'logins': LoginSchema(many=True).dump(results).data,
            'page': page,
            'limit': limit,
            'total': login_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'logins.get_logins', page=page - 1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'logins.get_logins', page=page + 1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        return jsonify(output), 200
    else:
        return '', 204
