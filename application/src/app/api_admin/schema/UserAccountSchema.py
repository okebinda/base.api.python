from marshmallow import fields, validate

from app import ma
from app.models.Administrator import Administrator
from app.lib.datetime.Formats import Formats


class UserAccountSchema(ma.Schema):

    class Meta:
        model = Administrator

        # fields to expose
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'uri', 'password_changed_at', 'joined_at')
        dump_only = ['joined_at']

    # hyperlinks
    uri = ma.AbsoluteUrlFor('administrators.get_administrator', administrator_id='<id>')

    # field validation
    id = fields.Integer()
    username = fields.String(
        required=True,
        validate=[
            validate.Length(2, 40, "Value must be between 2 and 40 characters long."),
            validate.Regexp('(?!^\d+$)^.+$', 0, 'Value must not be a number.'),
            validate.Regexp('^\w+$', 0, 'Value must contain only alphanumeric characters and the underscore.'),
        ])
    email = fields.Email(required=True)
    first_name = fields.String(
        required=True, validate=validate.Length(1, 40,
        "Value must be between 1 and 40 characters long."))
    last_name = fields.String(
        required=True, validate=validate.Length(2, 40,
        "Value must be between 2 and 40 characters long."))
    password_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    joined_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
