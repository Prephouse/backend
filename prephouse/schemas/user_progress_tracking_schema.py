from marshmallow import Schema, fields


class UserProgressTrackingQuestionRequestSchema(Schema):
    session_id = fields.Str(required=True)


class UserProgressTrackingSessionRequestSchema(Schema):
    session_id = fields.Str(required=True)


class UserProgressTrackingQuestionResponseSchema(Schema):
    session_id = fields.Str(required=True)
    question_id = fields.Str(required=True)
    score = fields.Str(required=True)
    # score = fields.Dict(keys=fields.Int(), values=fields.Str())(required=True)


class UserProgressTrackingSessionResponseSchema(Schema):
    session_id = fields.Str(required=True)
    score = fields.Str(required=True)
    # score = fields.Dict(keys=fields.Int(), values=fields.Str())(required=True)


class UserProgressTrackingOverallScoreSessionResponseSchema(Schema):
    session_id = fields.Str(required=True)
    score = fields.Float(required=True)


user_progress_tracking_question_request = UserProgressTrackingQuestionRequestSchema()
user_progress_tracking_session_request = UserProgressTrackingSessionRequestSchema()
user_progress_tracking_question_response = UserProgressTrackingQuestionResponseSchema()
user_progress_tracking_session_response = UserProgressTrackingSessionResponseSchema(many=True)
user_progress_tracking_overall_score_session_response = (
    UserProgressTrackingOverallScoreSessionResponseSchema()
)
