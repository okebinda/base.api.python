from marshmallow import fields

from app import ma
from app.models.Country import Country

class CountrySchema(ma.Schema):

    class Meta:
        model = Country

        # fields to expose
        fields = ('id', 'name', 'code_2', 'code_3', 'regions_uri')

    # hyperlinks
    regions_uri = ma.AbsoluteUrlFor('regions.get_regions', country_code='<code_2>')

    # field validation
    id = fields.Integer()
    name = fields.String()
    code_2 = fields.String()
    code_3 = fields.String()
