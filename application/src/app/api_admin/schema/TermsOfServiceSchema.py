from marshmallow import fields, validate

from app import ma
from app.models.TermsOfService import TermsOfService
from app.lib.datetime.Formats import Formats


class TermsOfServiceSchema(ma.Schema):

    class Meta:
        model = TermsOfService

        # fields to expose
        fields = ('id', 'text', 'version', 'publish_date', 'status',
                  'status_changed_at', 'created_at', 'updated_at')

    # field validation
    id = fields.Integer()
    text = fields.String(required=True)
    version = fields.String(
        required=True, validate=validate.Length(1, 10,
        "Value must be between 1 and 10 characters long."))
    publish_date = fields.DateTime(required=True, format=Formats.ISO_8601_DATETIME)
    status = fields.Integer(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
