from marshmallow import fields, validate

from app import ma
from app.models.AppKey import AppKey
from app.lib.datetime.Formats import Formats


class AppKeySchema(ma.Schema):

    class Meta:
        model = AppKey

        # fields to expose
        fields = ('id', 'application', 'key', 'status', 'status_changed_at',
                  'created_at', 'updated_at')

    # field validation
    id = fields.Integer()
    application = fields.String(
        required=True,
        validate=validate.Length(
            2, 200, "Value must be between 2 and 200 characters long."))
    key = fields.String(
        required=True,
        validate=validate.Length(32, 32, "Value must be 32 characters long."))
    status = fields.Integer(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
