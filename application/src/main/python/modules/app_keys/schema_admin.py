"""
Schemas to serialize/deserialize/validate models for App Keys module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from marshmallow import fields, validate

from init_dep import ma
from lib.datetime import Formats
from .model import AppKey


class AppKeyAdminSchema(ma.Schema):
    """Admin schema for AppKey model"""

    class Meta:
        """AppKeyAdminSchema meta data"""

        model = AppKey

        # fields to expose
        fields = ('id', 'application', 'key', 'status', 'status_changed_at',
                  'created_at', 'updated_at')

    # field validation
    id = fields.Integer()
    application = fields.String(
        required=True,
        validate=validate.Length(
            2, 200,
            error="Value must be between 2 and 200 characters long."))
    key = fields.String(
        required=True,
        validate=validate.Length(
            32, 32,
            error="Value must be 32 characters long."))
    status = fields.Integer(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
