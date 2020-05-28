"""
Schemas to serialize/deserialize/validate models in admin controllers for for
the Terms of Service module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from marshmallow import fields, validate

from init_dep import ma
from lib.datetime import Formats
from .model import TermsOfService


class TermsOfServiceAdminSchema(ma.Schema):
    """Admin schema for TermsOfService model"""

    class Meta:
        """TermsOfServiceAdminSchema meta data"""

        model = TermsOfService

        # fields to expose
        fields = ('id', 'text', 'version', 'publish_date', 'status',
                  'status_changed_at', 'created_at', 'updated_at')

    # field validation
    id = fields.Integer()
    text = fields.String(required=True)
    version = fields.String(
        required=True,
        validate=validate.Length(
            1, 10,
            error="Value must be between 1 and 10 characters long."))
    publish_date = fields.DateTime(
        required=True, format=Formats.ISO_8601_DATETIME)
    status = fields.Integer(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
