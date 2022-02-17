from marshmallow import Schema
from webargs import fields, validate

from prephouse.models import Feedback, Upload
from prephouse.utils import constants


class UploadRequestSchema(Schema):
    page = fields.Int(missing=1)


class UploadResponseSchema(Schema):
    class SingleUploadSchema(Schema):
        id = fields.UUID(required=True)
        category = fields.Int(
            validate=validate.OneOf(list(map(int, Upload.UploadCategory))),
            required=True,
        )
        date_uploaded = fields.DateTime(required=True)
        score = fields.Float()

    page = fields.Int(required=True)
    has_next = fields.Bool(required=True)
    uploads = fields.List(fields.Nested(SingleUploadSchema), required=True)


class FeedbackRequestSchema(Schema):
    # upload_ids = fields.DelimitedList(fields.UUID, required=True)
    time_start = fields.Int(missing=0)
    time_end = fields.Int(missing=constants.PSQL_INT_MAX)
    category = fields.Int(
        validate=validate.OneOf(list(map(int, Feedback.FeedbackCategory))),
        missing=None,
    )


class FeedbackResponseSchema(Schema):
    id = fields.Int(required=True)
    upload_id = fields.Int(required=True)
    category = fields.Int(
        required=True, validate=validate.OneOf(list(map(int, Feedback.FeedbackCategory)))
    )
    subcategory = fields.Str()
    comment = fields.Str()
    result = fields.Float(required=True)
    time_start = fields.Int()
    time_end = fields.Int()


upload_request_schema = UploadRequestSchema()
upload_response_schema = UploadResponseSchema()
feedback_request_schema = FeedbackRequestSchema()
feedback_response_schema = FeedbackResponseSchema(many=True)
