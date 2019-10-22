from marshmallow import fields

from app import ma
from app.models import UserTermsOfService
from app.lib.datetime import Formats

class UserTermsOfServiceSchema(ma.Schema):

    class Meta:
        model = UserTermsOfService

        # fields to expose
        fields = ('user_id', 'terms_of_service_id', 'accept_date', 'ip_address',
                  'created_at', 'updated_at', 'user', 'terms_of_service')
        load_only = ['user_id', 'terms_of_service_id']

    # nested schema
    user = fields.Nested(
        'UserSchema', exclude=('status', 'status_changed_at', 'created_at',
        'updated_at',), many=False)
    terms_of_service = fields.Nested(
        'TermsOfServiceSchema', exclude=('text', 'publish_date', 'status',
        'status_changed_at', 'created_at', 'updated_at',), many=False)

    # field validation
    user_id = fields.Integer(required=True)
    terms_of_service_id = fields.Integer(required=True)
    accept_date = fields.DateTime(required=True, format=Formats.ISO_8601_DATETIME)
    ip_address = fields.String(required=True)
    created_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
    updated_at = fields.DateTime(format=Formats.ISO_8601_DATETIME)
