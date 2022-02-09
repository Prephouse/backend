from marshmallow import Schema, fields


class UserProgressTrackingRequestSchema(Schema):
    session_id = fields.Int(required=True)
    question_id = fields.Int(required=True)


class UserProgressTrackingResponseSchema(Schema):
    id = fields.Int(required=True)
    score = fields.Float(required=True)


user_progress_tracking_request = UserProgressTrackingRequestSchema()
user_progress_tracking_response = UserProgressTrackingResponseSchema(many=True)
