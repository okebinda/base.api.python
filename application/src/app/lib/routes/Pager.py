"""Routing helper class for paging results"""

from flask import url_for


class Pager:
    """Helper for paging results"""

    @staticmethod
    def update(output, endpoint, page, limit, request_args, **kwargs):
        """Adds pager URIs (previous and next) to an output dictionary.

        :param output: A dictionary to be converted to JSON for output
        :type output: dict
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

        args = {k: v for (k, v) in request_args.items() if k != 'app_key'}
        Pager._add_previous(output, endpoint, page, limit, args, **kwargs)
        Pager._add_next(output, endpoint, page, limit, args, **kwargs)

    @staticmethod
    def _add_previous(output, endpoint, page, limit, request_args, **kwargs):
        """Adds a previous URI to an output dictionary.

        :param output: A dictionary to be converted to JSON for output
        :type output: dict
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

        if page != 1:
            output['previous_uri'] = url_for(endpoint, page=page - 1,
                                             limit=limit, _external=True,
                                             **kwargs, **request_args)

    @staticmethod
    def _add_next(output, endpoint, page, limit, request_args, **kwargs):
        """Adds a next URI to an output dictionary.

        :param output: A dictionary to be converted to JSON for output
        :type output: dict
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

        if page < output['total'] / limit:
            output['next_uri'] = url_for(endpoint, page=page + 1, limit=limit,
                                         _external=True, **kwargs,
                                         **request_args)
