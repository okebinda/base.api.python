from flask import Blueprint, jsonify, request, url_for

from app.models import Country
from app.api_public.authentication import require_appkey
from app.api_public.schema import CountrySchema

countries = Blueprint('countries', __name__)

@countries.route("/countries", methods=['GET'])
@countries.route("/countries/<int:page>", methods=['GET'])
@countries.route("/countries/<int:page>/<int(min=1, max=250):limit>", methods=['GET'])
@require_appkey
def get_countries(page=1, limit=250):

    # initialize query
    country_query = Country.query.filter(
        Country.status == Country.STATUS_ENABLED)

    # initialize order options dict
    order_options = {
        'id.asc': Country.id.asc(),
        'id.desc': Country.id.desc(),
        'name.asc': Country.name.asc(),
        'name.desc': Country.name.desc(),
        'code_2.asc': Country.code_2.asc(),
        'code_2.desc': Country.code_2.desc(),
        'code_3.asc': Country.code_3.asc(),
        'code_3.desc': Country.code_3.desc(),
    }

    # determine order
    if request.args.get('order_by') in order_options:
        order_by = order_options[request.args.get('order_by')]
    else:
        order_by = Country.name.asc()

    # retrieve and return results
    countries = country_query.order_by(order_by).limit(limit).offset((page-1)*limit)
    if countries.count():

        # prep initial output
        output = {
            'countries': CountrySchema(many=True).dump(countries).data,
            'page': page,
            'limit': limit,
            'total': country_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'countries.get_countries', page=page-1, limit=limit, _external=True,
                order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'countries.get_countries', page=page+1, limit=limit, _external=True,
                order_by=request.args.get('order_by', None))
        return jsonify(output), 200
    else:
        return '', 204
