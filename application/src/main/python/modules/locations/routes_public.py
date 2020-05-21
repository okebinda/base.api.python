"""
Public controllers for the Locations module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify, request

from lib.routes.pager import Pager
from lib.routes.query import Query
from .model import Country, Region
from .schema_public import CountrySchema, RegionSchema


def get_countries(page=1, limit=250):
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
        Country.name.asc(),
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
        Query.STATUS_FILTER_USER)

    # retrieve and return results
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'countries': CountrySchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(Pager.get_uris('public_locations.get_countries', page,
                                     limit, output['total'], request.args))
        return jsonify(output), 200

    return '', 204


def get_regions(country_code, page=1, limit=100):
    """Retrieves a list of regions (states).

    :param country_code: The two character country code to filter regions by
    :type country_code: str
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
        Region.name.asc(),
        {
            'id.asc': Region.id.asc(),
            'id.desc': Region.id.desc(),
            'name.asc': Region.name.asc(),
            'name.desc': Region.name.desc(),
            'code_2.asc': Region.code_2.asc(),
            'code_2.desc': Region.code_2.desc(),
        },
        request.args,
        Query.STATUS_FILTER_USER)

    query = query.filter(Region.country.has(code_2=country_code))

    # retrieve and return results
    results = list(query.limit(limit).offset((page - 1) * limit))
    if len(results) > 0:

        # prep initial output
        output = {
            'regions': RegionSchema(many=True).dump(results),
            'page': page,
            'limit': limit,
            'total': query.count()
        }

        # add pagination URIs and return
        output.update(
            Pager.get_uris('public_locations.get_regions', page, limit,
                           output['total'], request.args,
                           country_code=country_code))
        return jsonify(output), 200

    return '', 204
