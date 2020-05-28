"""
Schemas to serialize/deserialize/validate models in public controllers for
the Terms of Service module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from marshmallow import fields

from init_dep import ma
from lib.datetime import Formats
from .model import TermsOfService


class TermsOfServiceSchema(ma.Schema):
    """Public schema for TermsOfService model"""

    class Meta:
        """TermsOfServiceSchema meta data"""

        model = TermsOfService

        # fields to expose
        fields = ('id', 'text', 'version', 'publish_date')

    # field validation
    id = fields.Integer()
    text = fields.String()
    version = fields.String()
    publish_date = fields.DateTime(format=Formats.ISO_8601_DATETIME)
