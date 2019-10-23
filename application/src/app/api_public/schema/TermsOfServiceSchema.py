"""Schema to serialize/deserialize/validate TermsOfService model"""

from marshmallow import fields

from app import ma
from app.models.TermsOfService import TermsOfService
from app.lib.datetime.Formats import Formats


class TermsOfServiceSchema(ma.Schema):
    """Schema for TermsOfService model"""

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
