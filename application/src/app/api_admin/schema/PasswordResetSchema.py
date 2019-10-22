from marshmallow import fields, validate

from app import ma
from app.models.PasswordReset import PasswordReset
from app.lib.datetime.Formats import Formats


class PasswordResetSchema(ma.Schema):

    class Meta:
        model = PasswordReset

        # fields to expose
        fields = ('id', 'user_id', 'code', 'is_used', 'requested_at', 'status',
                  'status_changed_at', 'created_at', 'updated_at', 'user',
                  'ip_address')
        load_only = ['user_id']

    # nested schema
    user = fields.Nested('UserSchema', only=('id', 'username', 'uri'))

    # field validation
    id = fields.Integer()
    user_id = fields.Integer()
    code = fields.String(required=True, validate=validate.Length(1, 40,
        "Value must be between 6 and 40 characters long."))
    is_used = fields.Boolean(required=True)
    requested_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    ip_address = fields.String(required=True, validate=validate.Length(6, 50,
        "Value must be between 6 and 50 characters long."))
    status = fields.Integer(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
