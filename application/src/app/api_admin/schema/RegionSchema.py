"""Schema to serialize/deserialize/validate Region model"""

from marshmallow import fields, validate

from app import ma
from app.models.Region import Region
from app.lib.datetime.Formats import Formats


class RegionSchema(ma.Schema):
    """Schema for Region model"""

    class Meta:
        """RegionSchema meta data"""

        model = Region

        # fields to expose
        fields = ('id', 'name', 'code_2', 'country', 'status',
                  'status_changed_at', 'created_at', 'updated_at',
                  'country_id')
        load_only = ['country_id']

    # nested schema
    country = fields.Nested(
        'CountrySchema',
        exclude=('status', 'status_changed_at', 'created_at', 'updated_at'))

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
