from marshmallow import Schema, validate
from webargs import fields, validate

from prephouse.models import Upload


class NewUploadSessionRecordRequestSchema(Schema):
    category = fields.Int(
        validate=validate.OneOf(list(map(int, Upload.UploadCategory))),
        required=True,
    )


class NewUploadSessionRecordResponseSchema(Schema):
    id = fields.UUID(required=True)


class NewQuestionUploadIdRequestSchema(Schema):
    upload_id = fields.UUID(required=True)


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


upload_instructions_request_schema = UploadInstructionsRequestSchema()
upload_instructions_response_schema = UploadInstructionsResponseSchema()
new_question_upload_id_request_schema = NewQuestionUploadIdRequestSchema()
new_question_upload_id_response_schema = NewQuestionUploadIdResponseSchema()
new_upload_session_record_request_schema = NewUploadSessionRecordRequestSchema()
new_upload_session_record_response_schema = NewUploadSessionRecordResponseSchema()
