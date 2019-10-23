"""Schema to serialize/deserialize/validate Country model"""

from marshmallow import fields, validate

from app import ma
from app.models.Country import Country
from app.lib.datetime.Formats import Formats


class CountrySchema(ma.Schema):
    """Schema for Country model"""

    class Meta:
        """CountrySchema meta data"""

        model = Country

        # fields to expose
        fields = ('id', 'name', 'code_2', 'code_3', 'status',
                  'status_changed_at', 'created_at', 'updated_at')

    # field validation
    id = fields.Integer()
    name = fields.String(
        required=True,
        validate=validate.Length(
            2, 60, "Value must be between 2 and 60 characters long."))
    code_2 = fields.String(
        required=True,
        validate=validate.Length(2, 2, "Value must be 2 characters long."))
    code_3 = fields.String(
        required=True,
        validate=validate.Length(3, 3, "Value must be 3 characters long."))
    status = fields.Integer(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
