from marshmallow import Schema
from webargs import fields


class AnalysisRequestSchema(Schema):
    upload_question_id = fields.UUID(required=True)
    audio_link = fields.Str(required=True)
    transcript_link = fields.Str(required=True)
    video_link = fields.Str(missing=None)

class AnalysisResponseSchema(Schema):
    pass


analysis_request_schema = AnalysisRequestSchema()
analysis_response_schema = AnalysisResponseSchema()
