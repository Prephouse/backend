from marshmallow import Schema, fields


class AnalysisRequestSchema(Schema):
    upload_link = fields.Str(required=True)


class AnalysisResponseSchema(Schema):
    pass


analysis_request_schema = AnalysisRequestSchema()
analysis_response_schema = AnalysisResponseSchema()
