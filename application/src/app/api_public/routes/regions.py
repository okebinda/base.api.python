"""Regions controller"""

from flask import Blueprint, jsonify, request

from app.models.Region import Region
from app.api_public.authentication import require_appkey
from app.api_public.schema.RegionSchema import RegionSchema
from app.lib.routes.Pager import Pager

regions = Blueprint('regions', __name__)


@regions.route("/regions/<string:country_code>", methods=['GET'])
@regions.route("/regions/<string:country_code>/<int:page>", methods=['GET'])
@regions.route(
    "/regions/<string:country_code>/<int:page>/<int(min=1, max=250):limit>",
    methods=['GET'])
@require_appkey
def get_regions(country_code, page=1, limit=100):
    """Retrieves a list of regions (states)

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of regions; status code
    :rtype: (str, int)
    """

    # initialize query
    region_query = Region.query.filter(
        Region.status == Region.STATUS_ENABLED,
        Region.country.has(code_2=country_code))

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
        order_by = Region.name.asc()

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

        # add pagination URIs and return
        output.update(
            Pager.get_uris('regions.get_regions', page, limit, output['total'],
                           request.args, country_code=country_code))
        return jsonify(output), 200
    else:
        return '', 204
