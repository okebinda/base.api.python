from flask import Blueprint, jsonify, request, url_for

from app.models.Region import Region
from app.api_public.authentication import require_appkey
from app.api_public.schema.RegionSchema import RegionSchema

regions = Blueprint('regions', __name__)


@regions.route("/regions/<string:country_code>", methods=['GET'])
@regions.route("/regions/<string:country_code>/<int:page>", methods=['GET'])
@regions.route("/regions/<string:country_code>/<int:page>/<int(min=1, max=250):limit>", methods=['GET'])
@require_appkey
def get_regions(country_code, page=1, limit=100):

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
    regions = region_query.order_by(order_by).limit(limit).offset((page-1)*limit)
    if regions.count():

        # prep initial output
        output = {
            'regions': RegionSchema(many=True).dump(regions).data,
            'page': page,
            'limit': limit,
            'total': region_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'regions.get_regions', country_code=country_code, page=page-1,
                limit=limit, _external=True, order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'regions.get_regions', country_code=country_code, page=page+1,
                limit=limit, _external=True, order_by=request.args.get('order_by', None))
        return jsonify(output), 200
    else:
        return '', 204
