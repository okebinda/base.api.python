"""
Health Check public controllers.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify


def get_health_check():
    """Performs a basic system health check/smoke test.

    :returns: JSON string; status code
    :rtype: (str, int)
    """
    return jsonify({"success": True}), 200
