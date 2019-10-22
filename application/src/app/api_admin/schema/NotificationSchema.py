from marshmallow import fields, validate

from app import ma
from app.models.Notification import Notification
from app.lib.datetime.Formats import Formats


class NotificationSchema(ma.Schema):

    class Meta:
        model = Notification

        # fields to expose
        fields = ('id', 'user_id', 'channel', 'template', 'service',
                  'notification_id', 'accepted', 'rejected', 'sent_at', 'status',
                  'status_changed_at', 'created_at', 'updated_at', 'user')
        load_only = ['user_id']

    # nested schema
    user = fields.Nested('UserSchema', only=('id', 'username', 'uri'))

    # field validation
    id = fields.Integer()
    user_id = fields.Integer(required=False)
    channel = fields.Integer(required=True)
    template = fields.String(required=False, validate=validate.Length(0, 60,
        "Value must be between 0 and 60 characters long."))
    service = fields.String(required=False, validate=validate.Length(0, 60,
        "Value must be between 0 and 60 characters long."))
    notification_id = fields.String(required=False, validate=validate.Length(0, 60,
        "Value must be between 0 and 60 characters long."))
    accepted = fields.Integer(required=True)
    rejected = fields.Integer(required=True)
    sent_at = fields.DateTime(required=True, format=Formats.ISO_8601_DATETIME)
    status = fields.Integer(required=True)
    status_changed_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
