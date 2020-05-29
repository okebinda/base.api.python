"""
Public schemas to serialize/deserialize/validate models for Locations module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from marshmallow import fields

from init_dep import ma
from .model import Country, Region


class CountrySchema(ma.Schema):
    """Schema for Country model"""

    class Meta:
        """CountrySchema meta data"""

        model = Country

        # fields to expose
        fields = ('id', 'name', 'code_2', 'code_3', 'regions_uri')

    # hyperlinks
    regions_uri = ma.AbsoluteUrlFor('public_locations.get_regions',
                                    country_code='<code_2>')

    # field validation
    id = fields.Integer()
    name = fields.String()
    code_2 = fields.String()
    code_3 = fields.String()


class RegionSchema(ma.Schema):
    """Schema for Region model"""

    class Meta:
        """RegionSchema meta data"""

        model = Region

        # fields to expose
        fields = ('id', 'name', 'code_2')

    # field validation
    id = fields.Integer()
    name = fields.String()
    code_2 = fields.String()
