"""
Schemas to serialize/deserialize/validate models for the Password Resets
module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from marshmallow import fields, validate

from init_dep import ma
from lib.datetime import Formats
from .model import PasswordReset


class PasswordResetSchema(ma.Schema):
    """Schema for PasswordReset model"""

    class Meta:
        """PasswordResetSchema meta data"""

        model = PasswordReset

        # fields to expose
        fields = ('id', 'user_id', 'code', 'is_used', 'requested_at', 'status',
                  'status_changed_at', 'created_at', 'updated_at', 'user',
                  'ip_address')
        load_only = ['user_id']

    # nested schema
    user = fields.Nested('UserSchema', only=('id', 'username', 'uri'))

    # field validation
    id = fields.Integer()
    user_id = fields.Integer()
    code = fields.String(
        required=True,
        validate=validate.Length(
            1, 40,
            error="Value must be between 6 and 40 characters long."))
    is_used = fields.Boolean(required=True)
    requested_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    ip_address = fields.String(
        required=True,
        validate=validate.Length(
            6, 50,
            error="Value must be between 6 and 50 characters long."))
    status = fields.Integer(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
