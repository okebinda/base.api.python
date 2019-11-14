"""Regions controller"""

from flask import Blueprint, jsonify, request

from app.models.Region import Region
from app.api_admin.authentication import auth, admin_permission,\
    require_appkey, check_password_expiration
from app.api_admin.schema.RegionSchema import RegionSchema
from app.lib.routes.Pager import Pager
from app.lib.routes.Query import Query

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
    query = Query.make(
        Region,
        Region.id.asc(),
        {
            'id.asc': Region.id.asc(),
            'id.desc': Region.id.desc(),
            'name.asc': Region.name.asc(),
            'name.desc': Region.name.desc(),
            'code_2.asc': Region.code_2.asc(),
            'code_2.desc': Region.code_2.desc(),
        },
        request.args,
        Query.STATUS_FILTER_ADMIN)

    # filter query based on URL parameters
    if request.args.get('country_id', '').isnumeric():
        query = query.filter(
            Region.country_id == int(request.args.get('country_id')))

    # retrieve and return results
    results = query.limit(limit).offset((page - 1) * limit)
    if results.count():

        # prep initial output
        output = {
            'regions': RegionSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(Pager.get_uris('regions.get_regions', page, limit,
                                     output['total'], request.args))
        return jsonify(output), 200
    else:
        return '', 204
