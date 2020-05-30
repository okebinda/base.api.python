"""
Admin schemas to serialize/deserialize/validate models for the User Account
module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from marshmallow import fields, validate

from init_dep import ma
from lib.datetime import Formats
from modules.administrators.model import Administrator


class UserAccountAdminSchema(ma.Schema):
    """Schema for UserAccount model"""

    class Meta:
        """UserAccountAdminSchema meta data"""

        model = Administrator

        # fields to expose
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'uri', 'password_changed_at', 'joined_at')
        dump_only = ['id', 'uri', 'password_changed_at', 'joined_at']

    # hyperlinks
    uri = ma.AbsoluteUrlFor('admin_administrators.get_administrator',
                            administrator_id='<id>')

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
    password_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    joined_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
