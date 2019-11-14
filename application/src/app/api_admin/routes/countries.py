"""Countries controller"""

from flask import Blueprint, jsonify, request

from app.models.Country import Country
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.CountrySchema import CountrySchema
from app.lib.routes.Pager import Pager
from app.lib.routes.Query import Query

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
    """Retrieves a list of countries

    :param page: Page number
    :type page: int
    :param limit: Maximum number of results to show
    :type limit: int
    :returns: JSON string of list of countries; status code
    :rtype: (str, int)
    """

    # initialize query
    query = Query.make(
        Country,
        Country.id.asc(),
        {
            'id.asc': Country.id.asc(),
            'id.desc': Country.id.desc(),
            'name.asc': Country.name.asc(),
            'name.desc': Country.name.desc(),
            'code_2.asc': Country.code_2.asc(),
            'code_2.desc': Country.code_2.desc(),
            'code_3.asc': Country.code_3.asc(),
            'code_3.desc': Country.code_3.desc(),
        },
        request.args,
        Query.STATUS_FILTER_ADMIN)

    # retrieve and return results
    results = query.limit(limit).offset((page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'countries': CountrySchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(Pager.get_uris('countries.get_countries', page, limit,
                                     output['total'], request.args))
        return jsonify(output), 200
    else:
        return '', 204
