from marshmallow import Schema, fields


class UserProgressTrackingQuestionRequestSchema(Schema):
    question_id = fields.Int(required=True)


class UserProgressTrackingSessionRequestSchema(Schema):
    session_id = fields.Str(required=True)


class UserProgressTrackingResponseSchema(Schema):
    id = fields.Str(required=True)
    score = fields.Float(required=True)


user_progress_tracking_question_request = UserProgressTrackingQuestionRequestSchema()
user_progress_tracking_session_request = UserProgressTrackingSessionRequestSchema()
user_progress_tracking_response = UserProgressTrackingResponseSchema(many=True)
