"""
Error handlers.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=unused-argument

from flask import jsonify, make_response


def error_400(error):
    """400 error handler.

    :param error: Error type
    :type error: BadRequest
    :returns: JSON string of error response; status code
    :rtype: (str, int)
    """
    return make_response(jsonify({'error': 'Bad data'}), 400)


def error_401(error):
    """401 error handler.

    :param error: Error type
    :type error: Unauthorized
    :returns: JSON string of error response; status code
    :rtype: (str, int)
    """
    return make_response(jsonify({'error': 'Unauthorized'}), 401)


def error_403(error):
    """403 error handler.

    :param error: Error type
    :type error: Forbidden
    :returns: JSON string of error response; status code
    :rtype: (str, int)
    """
    return make_response(jsonify({'error': "Permission denied"}), 403)


def error_404(error):
    """404 error handler.

    :param error: Error type
    :type error: NotFound
    :returns: JSON string of error response; status code
    :rtype: (str, int)
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


def error_405(error):
    """405 error handler.

    :param error: Error type
    :type error: MethodNotAllowed
    :returns: JSON string of error response; status code
    :rtype: (str, int)
    """
    return make_response(jsonify({'error': 'Method not allowed'}), 405)


def error_500(error):
    """500 error handler.

    :param error: Error type
    :type error: InternalServerError
    :returns: JSON string of error response; status code
    :rtype: (str, int)
    """
    return make_response(jsonify({'error': 'Server error'}), 500)
