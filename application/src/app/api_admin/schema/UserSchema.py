from marshmallow import fields, validate

from app import ma
from app.models.User import User
from .UserTermsOfServiceSchema import UserTermsOfServiceSchema
from app.lib.datetime.Formats import Formats


class UserSchema(ma.Schema):

    # Rules:
    #  1) 3 out of 4:
    #    a) Upper case
    #    b) Lower case
    #    c) Number
    #    d) Non-alpha character
    #  2) 8-40 characters
    rePassword = r'^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{8,40}$'

    class Meta:
        model = User

        # fields to expose
        fields = ('id', 'username', 'email', 'roles', 'status',
                  'status_changed_at', 'uri', 'created_at', 'updated_at',
                  'password', 'terms_of_services', 'password_changed_at',
                  'profile', 'is_verified')
        load_only = ['password']

    # hyperlinks
    uri = ma.AbsoluteUrlFor('users.get_user', user_id='<id>')

    # nested schema
    roles = fields.Nested(
        'RoleSchema',
        exclude=('login_lockout_policy', 'login_max_attempts',
                 'login_timeframe', 'login_ban_time', 'login_ban_by_ip',
                 'password_policy', 'password_reset_days',
                 'password_reuse_history', 'created_at', 'updated_at',
                 'is_admin_role', 'priority'),
        many=True,
        dump_only=True)
    terms_of_services = fields.Nested(
        UserTermsOfServiceSchema,
        exclude=('user', 'created_at', 'updated_at'),
        many=True,
        dump_only=True)
    profile = fields.Nested(
        'UserProfileSchema',
        only=('first_name', 'last_name', 'title'))

    # field validation
    id = fields.Integer()
    username = fields.String(
        required=True,
        validate=[
            validate.Length(2, 40, "Value must be between 2 and 40 characters long."),
            validate.Regexp(r'(?!^\d+$)^.+$', 0, 'Value must not be a number.'),
            validate.Regexp(r'^\w+$', 0, 'Value must contain only alphanumeric characters and the underscore.'),
        ])
    email = fields.Email(required=True)
    status = fields.Integer(required=True)
    password_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    is_verified = fields.Boolean(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    password = fields.String(
        required=True, validate=validate.Regexp(
            rePassword, 0, 'Please choose a more complex password.'))
