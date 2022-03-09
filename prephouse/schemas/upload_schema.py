from marshmallow import Schema
from webargs import fields, validate

from prephouse.models import Upload


class NewUploadSessionRequestSchema(Schema):
    category = fields.Int(
        validate=validate.OneOf(list(map(int, Upload.UploadCategory))),
        required=True,
    )
    token = fields.Str(required=True)


class NewUploadSessionResponseSchema(Schema):
    id = fields.UUID(required=True)


class NewQuestionUploadRequestSchema(Schema):
    upload_id = fields.UUID(required=True)
    question_id = fields.Int(missing=None)


class UploadCloudFrontURLRequestSchema(Schema):
    file = fields.Str(required=True)
    cloudfront = fields.Str(required=True)
    manifest = fields.Str(required=True)


class UploadCloudFrontURLResponseSchema(Schema):
    pass


class NewQuestionUploadResponseSchema(Schema):
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


new_upload_session_request_schema = NewUploadSessionRequestSchema()
new_upload_session_response_schema = NewUploadSessionResponseSchema()
new_question_upload_request_schema = NewQuestionUploadRequestSchema()
new_question_upload_response_schema = NewQuestionUploadResponseSchema()
upload_instructions_request_schema = UploadInstructionsRequestSchema()
upload_instructions_response_schema = UploadInstructionsResponseSchema()
upload_cloudfronturl_request_schema = UploadCloudFrontURLRequestSchema()
upload_cloudfronturl_response_schema = UploadCloudFrontURLResponseSchema()
