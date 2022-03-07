from marshmallow import Schema
from webargs import fields


class ProgressRequestSchema(Schema):
    session_id = fields.Str(required=True)


class ProgressResponseSchema(Schema):
    session_id = fields.Str(required=True)
    response_data = fields.Raw(required=True)


class SessionScoresRequestSchema(Schema):
    pass


class SessionResponseSchema(Schema):
    class TextSchema(Schema):
        comment = fields.String(required=True)
        category = fields.String(required=True)

    class ScoresSchema(Schema):
        overall_score = fields.Float(required=True)
        silent_pauses_score = fields.Float(required=True)
        volume_score = fields.Float(required=True)
        background_light_score = fields.Float(required=True)
        gaze_direction_score = fields.Float(required=True)
        emotion_score = fields.Float(required=True)
        pitch_score = fields.Float(required=True)
        filler_words_score = fields.Float(required=True)

    session_id = fields.Str(required=True)
    session_category = fields.String(required=True)
    date = fields.DateTime(required=True)
    scores = fields.Nested(ScoresSchema, required=True)
    cloudfront_url = fields.String(required=True)
    text_feedback = fields.List(fields.Nested(TextSchema), required=False)


class SessionScoresResponseSchema(Schema):
    sessions = fields.List(fields.Nested(SessionResponseSchema), required=True)


class CategoryScoresResponseSchema(Schema):
    class ScoresSchema(Schema):
        overall_scores = fields.List(fields.Float, required=True)
        silent_pauses_scores = fields.List(fields.Float, required=True)
        volume_scores = fields.List(fields.Float, required=True)
        background_light_scores = fields.List(fields.Float, required=True)
        gaze_direction_scores = fields.List(fields.Float, required=True)
        emotion_scores = fields.List(fields.Float, required=True)
        pitch_scores = fields.List(fields.Float, required=True)
        filler_words_scores = fields.List(fields.Float, required=True)

    dates = fields.List(fields.DateTime, required=True)
    scores = fields.Nested(ScoresSchema, required=True)


progress_request_schema = ProgressRequestSchema()
progress_response_schema = ProgressResponseSchema()
session_response_schema = SessionResponseSchema()
session_scores_request_schema = SessionScoresRequestSchema()
session_scores_response_schema = SessionScoresResponseSchema()
category_scores_response_schema = CategoryScoresResponseSchema()
