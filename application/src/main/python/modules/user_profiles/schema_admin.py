"""
Schemas to serialize/deserialize/validate models for the User Profiles module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from marshmallow import fields, validate

from init_dep import ma
from lib.datetime import Formats
from .model import UserProfile


class UserProfileSchema(ma.Schema):
    """Schema for UserProfile model"""

    class Meta:
        """UserProfileSchema meta data"""

        model = UserProfile

        # fields to expose
        fields = ('id', 'user_id', 'first_name', 'last_name', 'status',
                  'status_changed_at', 'created_at', 'updated_at',
                  'joined_at')

    # field validation
    id = fields.Integer()
    user_id = fields.Integer(required=True)
    first_name = fields.String(
        required=True,
        validate=validate.Length(
            1, 40,
            error="Value must be between 1 and 40 characters long."))
    last_name = fields.String(
        required=True,
        validate=validate.Length(
            2, 40,
            error="Value must be between 2 and 40 characters long."))
    joined_at = fields.DateTime(
        required=True, format=Formats.ISO_8601_DATETIME)
    status = fields.Integer(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
