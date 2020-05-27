"""
Schemas to serialize/deserialize/validate models for the Logins module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from marshmallow import fields, validate

from init_dep import ma
from lib.datetime import Formats
from .model import Login


class LoginSchema(ma.Schema):
    """Schema for Login model"""

    class Meta:
        """LoginSchema meta data"""

        model = Login

        # fields to expose
        fields = ('id', 'user_id', 'username', 'ip_address', 'api', 'success',
                  'attempt_date', 'created_at', 'updated_at')

    # field validation
    id = fields.Integer()
    user_id = fields.Integer()
    username = fields.String(
        required=True,
        validate=validate.Length(
            1, 40,
            error="Value must be between 1 and 40 characters long."))
    ip_address = fields.String(
        required=True,
        validate=validate.Length(
            6, 50,
            error="Value must be between 6 and 50 characters long."))
    api = fields.Integer(required=True)
    success = fields.Boolean(required=True)
    attempt_date = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
