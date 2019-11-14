"""Regions controller"""

from flask import Blueprint, jsonify, request, url_for

from app.models.Region import Region
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.RegionSchema import RegionSchema

regions = Blueprint('regions', __name__)


@regions.route("/regions", methods=['GET'])
@regions.route("/regions/<int:page>", methods=['GET'])
@regions.route("/regions/<int:page>/<int(min=1, max=250):limit>",
               methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_regions(page=1, limit=10):
    """Retrieves a list of regions

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of regions; status code
    :rtype: (str, int)
    """

    # initialize query
    region_query = Region.query

    # filter query based on URL parameters
    if request.args.get('country_id', '').isnumeric():
        region_query = region_query.filter(
            Region.country_id == int(request.args.get('country_id')))
    if request.args.get('status', '').isnumeric():
        region_query = region_query.filter(
            Region.status == int(request.args.get('status')))
    else:
        region_query = region_query.filter(
            Region.status.in_((Region.STATUS_ENABLED, Region.STATUS_DISABLED,
                               Region.STATUS_PENDING)))

    # initialize order options dict
    order_options = {
        'id.asc': Region.id.asc(),
        'id.desc': Region.id.desc(),
        'name.asc': Region.name.asc(),
        'name.desc': Region.name.desc(),
        'code_2.asc': Region.code_2.asc(),
        'code_2.desc': Region.code_2.desc(),
    }

    # determine order
    if request.args.get('order_by') in order_options:
        order_by = order_options[request.args.get('order_by')]
    else:
        order_by = Region.id.asc()

    # retrieve and return results
    results = region_query.order_by(order_by).limit(limit).offset(
        (page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'regions': RegionSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': region_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'regions.get_regions', page=page - 1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'regions.get_regions', page=page + 1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        return jsonify(output), 200
    else:
        return '', 204
