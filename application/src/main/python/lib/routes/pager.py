"""
Routing helper class for paging results.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=too-few-public-methods

from flask import url_for


class Pager:
    """Helper for paging results"""

    @staticmethod
    def get_uris(endpoint, page, limit, total, request_args, **kwargs):
        """Creates a dictionary with next/previous endpoints for a listing
        endpoint.

        :param endpoint: A Flask endpoint string used in url_for()
        :type endpoint: str
        :param page: The current listing page number
        :type page: int
        :param limit: The current listing results limit per page
        :type limit: int
        :param total: The total number of records for the current listing
        :type total: int
        :param request_args: The Flask Request.args object
        :type request_args: ImmutableMultiDict
        :param kwargs: Additional keyword arguments to pass to url_for()
        """

        output = {}
        args = {k: v for (k, v) in request_args.items() if k != 'app_key'}

        if page != 1:
            output['previous_uri'] = Pager._previous_uri(
                endpoint, page, limit, args, **kwargs)

        if page < total / limit:
            output['next_uri'] = Pager._next_uri(
                endpoint, page, limit, args, **kwargs)

        return output

    @staticmethod
    def _previous_uri(endpoint, page, limit, request_args, **kwargs):
        """Generates a previous URI for a listing endpoint

        :param endpoint: A Flask endpoint string used in url_for()
        :type endpoint: str
        :param page: The current listing page number
        :type page: int
        :param limit: The current listing results limit per page
        :type limit: int
        :param request_args: The Flask Request.args object
        :type request_args: ImmutableMultiDict
        :param kwargs: Additional keyword arguments to pass to url_for()
        """

        return url_for(endpoint, page=page - 1, limit=limit, _external=True,
                       **kwargs, **request_args)

    @staticmethod
    def _next_uri(endpoint, page, limit, request_args, **kwargs):
        """Generates a next URI for a listing endpoint.

        :param endpoint: A Flask endpoint string used in url_for()
        :type endpoint: str
        :param page: The current listing page number
        :type page: int
        :param limit: The current listing results limit per page
        :type limit: int
        :param request_args: The Flask Request.args object
        :type request_args: ImmutableMultiDict
        :param kwargs: Additional keyword arguments to pass to url_for()
        """

        return url_for(endpoint, page=page + 1, limit=limit, _external=True,
                       **kwargs, **request_args)
