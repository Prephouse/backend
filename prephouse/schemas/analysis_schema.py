from marshmallow import Schema
from webargs import fields


class AnalysisRequestSchema(Schema):
    upload_link = fields.Url(required=True)


class AnalysisResponseSchema(Schema):
    pass


analysis_request_schema = AnalysisRequestSchema()
analysis_response_schema = AnalysisResponseSchema()
