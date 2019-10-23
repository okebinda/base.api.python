"""Schema to serialize/deserialize/validate UserProfile model"""

from marshmallow import fields, validate

from app import ma
from app.models.UserProfile import UserProfile
from app.lib.datetime.Formats import Formats


class UserProfileSchema(ma.Schema):
    """Schema for UserProfile model"""

    class Meta:
        """UserProfileSchema meta data"""

        model = UserProfile

        # fields to expose
        fields = ('id', 'user_id', 'first_name', 'last_name', 'status',
                  'status_changed_at', 'created_at', 'updated_at',
                  'joined_at')

    # field validation
    id = fields.Integer()
    user_id = fields.Integer(required=True)
    first_name = fields.String(
        required=True,
        validate=validate.Length(
            1, 40, "Value must be between 1 and 40 characters long."))
    last_name = fields.String(
        required=True,
        validate=validate.Length(
            2, 40, "Value must be between 2 and 40 characters long."))
    joined_at = fields.DateTime(
        required=True, format=Formats.ISO_8601_DATETIME)
    status = fields.Integer(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
