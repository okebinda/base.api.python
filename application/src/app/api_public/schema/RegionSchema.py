from marshmallow import fields

from app import ma
from app.models.Region import Region


class RegionSchema(ma.Schema):

    class Meta:
        model = Region

        # fields to expose
        fields = ('id', 'name', 'code_2')

    # field validation
    id = fields.Integer()
    name = fields.String()
    code_2 = fields.String()
