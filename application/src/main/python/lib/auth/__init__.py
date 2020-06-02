"""
Authentication module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_principal import Permission, RoleNeed


auth_basic = HTTPBasicAuth()
auth_token = HTTPTokenAuth(scheme='Bearer')

permission_user = Permission(RoleNeed('USER'))
permission_super_admin = Permission(RoleNeed('SUPER_ADMIN'))
