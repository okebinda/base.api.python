"""
Admin schemas to serialize/deserialize/validate models for Locations module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from marshmallow import fields, validate

from init_dep import ma
from lib.datetime import Formats
from .model import Country, Region


class CountryAdminSchema(ma.Schema):
    """Schema for Country model"""

    class Meta:
        """CountryAdminSchema meta data"""

        model = Country

        # fields to expose
        fields = ('id', 'name', 'code_2', 'code_3', 'status',
                  'status_changed_at', 'created_at', 'updated_at')

    # field validation
    id = fields.Integer()
    name = fields.String(
        required=True,
        validate=validate.Length(
            2, 60,
            error="Value must be between 2 and 60 characters long."))
    code_2 = fields.String(
        required=True,
        validate=validate.Length(
            2, 2,
            error="Value must be 2 characters long."))
    code_3 = fields.String(
        required=True,
        validate=validate.Length(
            3, 3,
            error="Value must be 3 characters long."))
    status = fields.Integer(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)


class RegionAdminSchema(ma.Schema):
    """Schema for Region model"""

    class Meta:
        """RegionAdminSchema meta data"""

        model = Region

        # fields to expose
        fields = ('id', 'name', 'code_2', 'country', 'status',
                  'status_changed_at', 'created_at', 'updated_at',
                  'country_id')
        load_only = ['country_id']

    # nested schema
    country = fields.Nested(
        'CountryAdminSchema',
        only=('id', 'name', 'code_2', 'code_3'))

    # field validation
    id = fields.Integer()
    name = fields.String(
        required=True,
        validate=validate.Length(
            2, 60,
            error="Value must be between 2 and 60 characters long."))
    code_2 = fields.String(
        validate=validate.Length(
            2, 2,
            error="Value must be 2 characters long."))
    country_id = fields.Integer(required=True)
    status = fields.Integer(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
