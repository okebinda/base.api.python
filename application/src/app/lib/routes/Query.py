"""Routing helper class for managing SQLAlchemy queries"""


class Query:
    """Helper for database queries in routes"""

    STATUS_FILTER_NONE = 0
    STATUS_FILTER_USER = 1
    STATUS_FILTER_ADMIN = 2

    @staticmethod
    def make(model, default_order, order_options, request_args, status_filter):
        """Generates a query object for a sqlalchemy model with optional
        filtering by status.

        :param model: SQLAlchemy database model
        :type model: flask_sqlalchemy.Model
        :param default_order: The default query ordering
        :type default_order: sqlalchemy.sql.elements.UnaryExpression
        :param order_options: A mapping of order options: str->object
        :type order_options: dict
        :param request_args: The Flask Request.args object
        :type request_args: ImmutableMultiDict
        :param status_filter: Flag for status filtering behavior
        :type status_filter: int
        :return: The model's query object
        :rtype: flask_sqlalchemy.BaseQuery
        """

        # initialize query
        query = model.query

        # filter by status
        query = Query._filter_status(query, model, status_filter,
                                     request_args.get('status', None))

        # determine order
        query = Query._order_by(query, default_order, order_options,
                                request_args.get('order_by', None))

        return query

    @staticmethod
    def _filter_status(query, model, status_filter, status):
        """Adds filtering by status to query.

        :param query: The model's query object
        :type query: flask_sqlalchemy.BaseQuery
        :param model: SQLAlchemy database model
        :type model: flask_sqlalchemy.Model
        :return: The model's updated query object
        :param status_filter: Flag for status filtering behavior
        :type status_filter: int
        :param status: The status to filter by
        :type status: int
        :return: The model's updated query object
        :rtype: flask_sqlalchemy.BaseQuery
        """

        # filter query by status for a user
        if status_filter == Query.STATUS_FILTER_USER:
            return Query._filter_status_user(query, model)

        # filter query by status for an administrator
        elif status_filter == Query.STATUS_FILTER_ADMIN:
            return Query._filter_status_admin(query, model, status)

        # no status filtering
        return query

    @staticmethod
    def _filter_status_user(query, model):
        """Adds filtering by status to user query.

        :param query: The model's query object
        :type query: flask_sqlalchemy.BaseQuery
        :param model: SQLAlchemy database model
        :type model: flask_sqlalchemy.Model
        :return: The model's updated query object
        :rtype: flask_sqlalchemy.BaseQuery
        """

        return query.filter(model.status == model.STATUS_ENABLED)

    @staticmethod
    def _filter_status_admin(query, model, status):
        """Adds filtering by status to administrator query.

        :param query: The model's query object
        :type query: flask_sqlalchemy.BaseQuery
        :param model: SQLAlchemy database model
        :type model: flask_sqlalchemy.Model
        :param status: The status to filter by
        :type status: int
        :return: The model's updated query object
        :rtype: flask_sqlalchemy.BaseQuery
        """

        if status is not None and status.isnumeric():
            return query.filter(model.status == int(status))
        else:
            return query.filter(model.status.in_((model.STATUS_ENABLED,
                                                  model.STATUS_DISABLED,
                                                  model.STATUS_PENDING)))

    @staticmethod
    def _order_by(query, default_order, order_options, order_by):
        """Adds ordering to the query.

        :param query: The model's query object
        :type query: flask_sqlalchemy.BaseQuery
        :param default_order: The default query ordering
        :type default_order: sqlalchemy.sql.elements.UnaryExpression
        :param order_options: A mapping of order options: str->object
        :type order_options: dict
        :param order_by: The requested order
        :type order_by: str
        :return: The model's updated query object
        :rtype: flask_sqlalchemy.BaseQuery
        """
        if order_by in order_options:
            return query.order_by(order_options[order_by])
        else:
            return query.order_by(default_order)
