"""Schema to serialize/deserialize/validate Administrator model"""

from marshmallow import fields, validate, EXCLUDE

from app import ma
from app.models.Administrator import Administrator
from app.lib.datetime.Formats import Formats


class AdministratorSchema(ma.Schema):
    """Schema for Administrator model"""

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
        """AdministratorSchema meta data"""

        model = Administrator

        # fields to expose
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'roles', 'status', 'status_changed_at', 'uri', 'created_at',
                  'updated_at', 'password', 'password_changed_at', 'joined_at')
        load_only = ['password']
        unknown = EXCLUDE  # fix for `role` property after marshmallow 3

    # hyperlinks
    uri = ma.AbsoluteUrlFor(
        'administrators.get_administrator', administrator_id='<id>')

    # nested schema
    roles = fields.Nested(
        'RoleSchema', exclude=(
            'login_lockout_policy', 'login_max_attempts', 'login_timeframe',
            'login_ban_time', 'login_ban_by_ip', 'password_policy',
            'password_reset_days', 'password_reuse_history', 'created_at',
            'updated_at', 'is_admin_role', 'priority'),
        many=True, dump_only=True)

    # field validation
    id = fields.Integer()
    username = fields.String(
        required=True,
        validate=[
            validate.Length(
                2, 40,
                error="Value must be between 2 and 40 characters long."),
            validate.Regexp(
                r'(?!^\d+$)^.+$', 0,
                error='Value must not be a number.'),
            validate.Regexp(
                r'^\w+$', 0,
                error=''.join(["Value must contain only alphanumeric ",
                               "characters and the underscore."])),
        ])
    email = fields.Email(required=True)
    first_name = fields.String(
        required=True,
        validate=validate.Length(
            1, 40,
            error="Value must be between 1 and 40 characters long."))
    last_name = fields.String(
        required=True,
        validate=validate.Length(
            2, 40,
            error="Value must be between 2 and 40 characters long."))
    status = fields.Integer(required=True)
    password_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    joined_at = fields.DateTime(
        required=True, format=Formats.ISO_8601_DATETIME)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    password = fields.String(
        required=True,
        validate=validate.Regexp(
            re_password, 0,
            error='Please choose a more complex password.'))
