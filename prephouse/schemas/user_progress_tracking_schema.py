from marshmallow import Schema, fields, validate

from prephouse.models import Feedback


class UserProgressTrackingRequestSchema(Schema):
    session_id = fields.Int(required=True)
    question_id = fields.Int(required=True)


class UserProgressTrackingResponse(Schema):
    id = fields.Int(required=True)
    score = fields.Float(required=True)


user_progress_tracking_request = UserProgressTrackingRequestSchema()
user_progress_tracking_response = UserProgressTrackingResponse(many=True)
