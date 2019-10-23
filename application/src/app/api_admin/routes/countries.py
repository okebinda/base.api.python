from flask import Blueprint, jsonify, request, url_for

from app.models.Country import Country
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.CountrySchema import CountrySchema

countries = Blueprint('countries', __name__)


@countries.route("/countries", methods=['GET'])
@countries.route("/countries/<int:page>", methods=['GET'])
@countries.route("/countries/<int:page>/<int(min=1, max=250):limit>",
                 methods=['GET'])
@require_appkey
@auth.login_required
@admin_permission.require(http_exception=403)
@check_password_expiration
def get_countries(page=1, limit=10):

    # initialize query
    country_query = Country.query

    # filter query based on URL parameters
    if request.args.get('status', '').isnumeric():
        country_query = country_query.filter(
            Country.status == int(request.args.get('status')))
    else:
        country_query = country_query.filter(
            Country.status.in_((Country.STATUS_ENABLED,
                                Country.STATUS_DISABLED,
                                Country.STATUS_PENDING)))

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
        order_by = Country.id.asc()

    # retrieve and return results
    results = country_query.order_by(order_by).limit(limit).offset(
        (page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'countries': CountrySchema(many=True).dump(results).data,
            'page': page,
            'limit': limit,
            'total': country_query.count()
        }

        # prep pagination URIs
        if page != 1:
            output['previous_uri'] = url_for(
                'countries.get_countries', page=page - 1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        if page < output['total'] / limit:
            output['next_uri'] = url_for(
                'countries.get_countries', page=page + 1, limit=limit,
                _external=True, order_by=request.args.get('order_by', None))
        return jsonify(output), 200
    else:
        return '', 204
