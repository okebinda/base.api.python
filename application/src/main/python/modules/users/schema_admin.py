"""
Schemas to serialize/deserialize/validate models for the Users module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from marshmallow import fields, validate, EXCLUDE

from init_dep import ma
from lib.datetime import Formats
from .model import User, UserTermsOfService


class UserTermsOfServiceAdminSchema(ma.Schema):
    """Admin schema for UserTermsOfService model"""

    class Meta:
        """UserTermsOfServiceAdminSchema meta data"""

        model = UserTermsOfService

        # fields to expose
        fields = ('user_id', 'terms_of_service_id', 'accept_date',
                  'ip_address', 'created_at', 'updated_at', 'user',
                  'terms_of_service')
        load_only = ['user_id', 'terms_of_service_id']

    # nested schema
    user = fields.Nested(
        'UserAdminSchema',
        only=('id', 'username', 'uri'),
        many=False)
    terms_of_service = fields.Nested(
        'TermsOfServiceAdminSchema',
        only=('id', 'version'),
        many=False)

    # field validation
    user_id = fields.Integer(required=True)
    terms_of_service_id = fields.Integer(required=True)
    accept_date = fields.DateTime(required=True,
                                  format=Formats.ISO_8601_DATETIME)
    ip_address = fields.String(required=True)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)


class UserAdminSchema(ma.Schema):
    """Admin schema for User model"""

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
        """UserAdminSchema meta data"""

        model = User

        # fields to expose
        fields = ('id', 'username', 'email', 'roles', 'status',
                  'status_changed_at', 'uri', 'created_at', 'updated_at',
                  'password', 'terms_of_services', 'password_changed_at',
                  'profile', 'is_verified')
        load_only = ['password']
        dump_only = ['created_at', 'password_changed_at', 'status_changed_at',
                     'updated_at']
        unknown = EXCLUDE  # fix for `role` property after marshmallow 3

    # hyperlinks
    uri = ma.AbsoluteUrlFor('admin_users.get_user',
                            values=dict(user_id='<id>'))

    # nested schema
    roles = fields.Nested(
        'RoleAdminSchema',
        only=('id', 'name'),
        many=True,
        dump_only=True)
    terms_of_services = fields.Nested(
        'UserTermsOfServiceAdminSchema',
        only=('accept_date', 'ip_address', 'terms_of_service'),
        many=True,
        dump_only=True)
    profile = fields.Nested(
        'UserProfileAdminSchema',
        only=('first_name', 'last_name', 'joined_at'))

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
                               "characters and the underscore."]))
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
            re_password, 0,
            error='Please choose a more complex password.'))
