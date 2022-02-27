from marshmallow import Schema
from webargs import fields


class ProgressRequestSchema(Schema):
    session_id = fields.Str(required=True)


class ProgressResponseSchema(Schema):
    session_id = fields.Str(required=True)
    response_data = fields.Raw(required=True)


class AllScoresPerSessionRequestSchema(Schema):
    pass


class AllScoresPerSessionResponseSchema(Schema):
    class UploadEntrySchema(Schema):
        session_id = fields.UUID(required=True)
        session_category = fields.String(required=True)
        date = fields.DateTime(required=True)
        overall_score = fields.Float(required=True)
        silent_pauses_score = fields.Float(required=True)
        volume_score = fields.Float(required=True)
        background_light_score = fields.Float(required=True)
        gaze_direction_score = fields.Float(required=True)
        emotion_score = fields.Float(required=True)
        pitch_score = fields.Float(required=True)
        filler_words_score = fields.Float(required=True)

    sessions = fields.List(fields.Nested(UploadEntrySchema), required=True)


class AllScoresPerCategoryResponseSchema(Schema):
    dates = fields.List(fields.DateTime, required=True)
    overall_scores = fields.List(fields.Float, required=True)
    silent_pauses_scores = fields.List(fields.Float, required=True)
    volume_scores = fields.List(fields.Float, required=True)
    background_light_scores = fields.List(fields.Float, required=True)
    gaze_direction_scores = fields.List(fields.Float, required=True)
    emotion_scores = fields.List(fields.Float, required=True)
    pitch_scores = fields.List(fields.Float, required=True)
    filler_words_scores = fields.List(fields.Float, required=True)


progress_request = ProgressRequestSchema()
progress_response = ProgressResponseSchema()
all_scores_per_session_request = AllScoresPerSessionRequestSchema()
all_scores_per_session_response = AllScoresPerSessionResponseSchema()
all_scores_per_category_response = AllScoresPerCategoryResponseSchema()
