"""
Schemas to serialize/deserialize/validate models for Roles module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from marshmallow import fields, validate

from init_dep import ma
from lib.datetime import Formats
from .model import Role


class RoleAdminSchema(ma.Schema):
    """Admin schema for Role model"""

    class Meta:
        """RoleAdminSchema meta data"""

        model = Role

        # fields to expose
        fields = ('id', 'name', 'login_lockout_policy', 'login_max_attempts',
                  'login_timeframe', 'login_ban_time', 'login_ban_by_ip',
                  'password_policy', 'password_reuse_history',
                  'password_reset_days', 'created_at', 'updated_at',
                  'is_admin_role', 'priority')

    # field validation
    id = fields.Integer()
    name = fields.String(
        required=True,
        validate=validate.Length(
            2, 32,
            error="Value must be between 2 and 32 characters long."))
    is_admin_role = fields.Boolean(required=True)
    priority = fields.Integer(required=True)
    login_lockout_policy = fields.Boolean(required=True)
    login_max_attempts = fields.Integer(required=True)
    login_timeframe = fields.Integer(required=True)
    login_ban_time = fields.Integer(required=True)
    login_ban_by_ip = fields.Boolean(required=True)
    password_policy = fields.Boolean(required=True)
    password_reuse_history = fields.Integer(required=True)
    password_reset_days = fields.Integer(required=True)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
