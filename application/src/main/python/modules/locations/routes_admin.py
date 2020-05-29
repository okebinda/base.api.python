"""
Admin controllers for the Locations module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member

from flask import jsonify, request

from lib.routes.pager import Pager
from lib.routes.query import Query
from .model import Country, Region
from .schema_admin import CountryAdminSchema, RegionAdminSchema


def get_countries(page=1, limit=10):
    """Retrieves a list of countries.

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
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'countries': CountryAdminSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(Pager.get_uris('admin_locations.get_countries', page,
                                     limit, output['total'], request.args))
        return jsonify(output), 200

    return '', 204


def get_regions(page=1, limit=10):
    """Retrieves a list of regions.

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
    if request.args.get('country_id', None) is not None:
        query = query.filter(
            Region.country_id == int(request.args.get('country_id')))

    # retrieve and return results
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'regions': RegionAdminSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(Pager.get_uris('admin_locations.get_regions', page,
                                     limit, output['total'], request.args))
        return jsonify(output), 200

    return '', 204
