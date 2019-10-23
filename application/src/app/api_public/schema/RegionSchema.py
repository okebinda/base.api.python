"""Schema to serialize/deserialize/validate Region model"""

from marshmallow import fields

from app import ma
from app.models.Region import Region


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
