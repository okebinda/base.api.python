from flask import Blueprint, jsonify, request, url_for

from app.models.PasswordReset import PasswordReset
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.PasswordResetSchema import PasswordResetSchema

password_resets = Blueprint('password_resets', __name__)


@password_resets.route("/password_resets", methods=['GET'])
@password_resets.route("/password_resets/<int:page>", methods=['GET'])
@password_resets.route(
    "/password_resets/<int:page>/<int(min=1, max=100):limit>", methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_password_resets(page=1, limit=10):

    # initialize query
    password_reset_query = PasswordReset.query

    # filter query based on URL parameters
    if request.args.get('user_id', None) is not None:
        password_reset_query = password_reset_query.filter(
            PasswordReset.user_id == request.args.get('user_id'))
    if request.args.get('status', '').isnumeric():
        password_reset_query = password_reset_query.filter(
            PasswordReset.status == int(request.args.get('status')))
    else:
        password_reset_query = password_reset_query.filter(
            PasswordReset.status.in_((PasswordReset.STATUS_ENABLED,
                                      PasswordReset.STATUS_DISABLED,
                                      PasswordReset.STATUS_PENDING)))

    # initialize order options dict
    order_options = {
        'id.asc': PasswordReset.id.asc(),
        'id.desc': PasswordReset.id.desc(),
        'requested_at.asc': PasswordReset.requested_at.asc(),
        'requested_at.desc': PasswordReset.requested_at.desc(),
    }

    # determine order
    if request.args.get('order_by') in order_options:
        order_by = order_options[request.args.get('order_by')]
    else:
        order_by = PasswordReset.id.asc()

    # retrieve and return results
    results = password_reset_query.order_by(order_by).limit(
        limit).offset((page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'password_resets': PasswordResetSchema(many=True).dump(
                results).data,
            'page': page,
            'limit': limit,
            'total': password_reset_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'password_resets.get_password_resets',
                page=page - 1,
                limit=limit,
                _external=True,
                order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'password_resets.get_password_resets',
                page=page + 1,
                limit=limit,
                _external=True,
                order_by=request.args.get('order_by', None))
        return jsonify(output), 200
    else:
        return '', 204
