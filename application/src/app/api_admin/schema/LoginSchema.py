from marshmallow import fields, validate

from app import ma
from app.models.Login import Login
from app.lib.datetime.Formats import Formats


class LoginSchema(ma.Schema):

    class Meta:
        model = Login

        # fields to expose
        fields = ('id', 'user_id', 'username', 'ip_address', 'success',
                  'attempt_date', 'created_at', 'updated_at')

    # field validation
    id = fields.Integer()
    user_id = fields.Integer()
    username = fields.String(required=True, validate=validate.Length(1, 40,
        "Value must be between 1 and 40 characters long."))
    ip_address = fields.String(required=True, validate=validate.Length(6, 50,
        "Value must be between 6 and 50 characters long."))
    success = fields.Boolean(required=True)
    attempt_date = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
