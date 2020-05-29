"""
Authentication module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth


auth_basic = HTTPBasicAuth()
auth_token = HTTPTokenAuth(scheme='Bearer')
