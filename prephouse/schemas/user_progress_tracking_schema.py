from marshmallow import Schema
from webargs import fields


class UserProgressTrackingRequestSchema(Schema):
    session_id = fields.Str(required=True)


class UserProgressTrackingResponseSchema(Schema):
    session_id = fields.Str(required=True)
    response_data = fields.Raw(required=True)


user_progress_tracking_request = UserProgressTrackingRequestSchema()
user_progress_tracking_response = UserProgressTrackingResponseSchema()
