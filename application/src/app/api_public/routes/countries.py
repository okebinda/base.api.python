"""Countries controller"""

from flask import Blueprint, jsonify, request

from app.models.Country import Country
from app.api_public.authentication import require_appkey
from app.api_public.schema.CountrySchema import CountrySchema
from app.lib.routes.Pager import Pager

countries = Blueprint('countries', __name__)


@countries.route("/countries", methods=['GET'])
@countries.route("/countries/<int:page>", methods=['GET'])
@countries.route("/countries/<int:page>/<int(min=1, max=250):limit>",
                 methods=['GET'])
@require_appkey
def get_countries(page=1, limit=250):
    """Retrieves a list of countries

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of countries; status code
    :rtype: (str, int)
    """

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
    results = country_query.order_by(order_by).limit(limit).offset(
        (page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'countries': CountrySchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': country_query.count()
        }

        # add pagination URIs and return
        output.update(Pager.get_uris('countries.get_countries', page, limit,
                                     output['total'], request.args))
        return jsonify(output), 200
    else:
        return '', 204
