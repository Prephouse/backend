from marshmallow import Schema, validate
from webargs import fields

from prephouse.models import Upload


class NewQuestionUploadIdResponseSchema(Schema):
    id = fields.UUID(required=True)


class UploadInstructionsRequestSchema(Schema):
    category = fields.Int(
        validate=validate.OneOf(list(map(int, Upload.UploadCategory))),
        required=True,
    )
    medium = fields.Int(
        validate=validate.OneOf(list(map(int, Upload.UploadMedium))),
        required=True,
    )
    origin = fields.Int(
        validate=validate.OneOf(list(map(int, Upload.UploadOrigin))),
        required=True,
    )


class UploadInstructionsResponseSchema(Schema):
    feedback_categories = fields.List(fields.Str)
    overview = fields.Str()
    pre_analysis = fields.Str()
    post_analysis = fields.Str()
    confirmation = fields.Str()


new_question_upload_id_response_schema = NewQuestionUploadIdResponseSchema()
upload_instructions_request_schema = UploadInstructionsRequestSchema()
upload_instructions_response_schema = UploadInstructionsResponseSchema()
