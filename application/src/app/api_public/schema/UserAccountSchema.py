"""Schema to serialize/deserialize/validate UserAccount model"""

from marshmallow import fields, validate

from app import ma
from app.lib.datetime.Formats import Formats


class UserAccountSchema(ma.Schema):
    """Schema for UserAccount model"""

    # Rules:
    #  1) 3 out of 4:
    #    a) Upper case
    #    b) Lower case
    #    c) Number
    #    d) Non-alpha character
    #  2) 8-40 characters
    re_password = ''.join([
        r'^(?:',
        r'(?=.*[a-z])',
        r'(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))',
        r'|(?=.*\W)(?=.*[A-Z])(?=.*\d)',
        r').{8,40}$'
    ])

    class Meta:
        """UserAccountSchema meta data"""

        # fields to expose
        fields = ('id', 'username', 'email', 'password', 'password2', 'tos_id',
                  'first_name', 'last_name', 'password_changed_at',
                  'joined_at', 'is_verified')
        load_only = ['password', 'password2', 'tos_id']
        dump_only = ['joined_at', 'is_verified', 'password_changed_at']

    # field validation
    id = fields.Integer()
    username = fields.String(
        required=True,
        validate=[
            validate.Length(
                2, 40, "Value must be between 2 and 40 characters long."),
            validate.Regexp(
                r'(?!^\d+$)^.+$', 0, 'Value must not be a number.'),
            validate.Regexp(
                r'^\w+$', 0, ''.join(["Value must contain only alphanumeric ",
                                      "characters and the underscore."])),
        ])
    email = fields.Email(required=True)
    password = fields.String(
        required=True, validate=validate.Regexp(
            re_password, 0, 'Please choose a more complex password.'))
    password2 = fields.String(required=True)
    tos_id = fields.Integer(required=True)
    password_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    joined_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    is_verified = fields.Boolean()

    first_name = fields.String(
        required=True,
        validate=validate.Length(
            1, 40, "Value must be between 1 and 40 characters long."))
    last_name = fields.String(
        required=True,
        validate=validate.Length(
            2, 40, "Value must be between 2 and 40 characters long."))
