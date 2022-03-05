from marshmallow import Schema
from webargs import fields, validate

from prephouse.models import Feedback, Upload
from prephouse.utils import constants


class UploadRequestSchema(Schema):
    page = fields.Int(missing=1)
    per_page = fields.Int(missing=20)


class UploadResponseSchema(Schema):
    class SingleUploadSchema(Schema):
        id = fields.UUID(required=True)
        category = fields.Int(
            validate=validate.OneOf(list(map(int, Upload.UploadCategory))),
            required=True,
        )
        date_uploaded = fields.DateTime(required=True)
        score = fields.Float()

    next_page = fields.Int(required=True)
    has_next = fields.Bool(required=True)
    uploads = fields.List(fields.Nested(SingleUploadSchema), required=True)


class FeedbackRequestSchema(Schema):
    time_start = fields.Int(missing=0)
    time_end = fields.Int(missing=constants.PSQL_INT_MAX)
    category = fields.Int(
        validate=validate.OneOf(list(map(int, Feedback.FeedbackCategory))),
        missing=None,
    )


class FeedbackResponseSchema(Schema):
    class SingleFeedback(Schema):
        id = fields.UUID(required=True)
        feature_name = fields.Str(required=True)
        subcategory = fields.Str()
        comment = fields.Str()
        result = fields.Float(required=True)
        time_start = fields.Int()
        time_end = fields.Int()

    upload_id = fields.UUID(required=True)
    feedbacks = fields.Dict(
        keys=fields.Str(),
        values=fields.Dict(
            keys=fields.Int(
                required=True,
                validate=validate.OneOf(list(map(int, Feedback.FeedbackCategory))),
            ),
            values=fields.Nested(SingleFeedback),
        ),
        required=True,
    )


upload_request_schema = UploadRequestSchema()
upload_response_schema = UploadResponseSchema()
feedback_request_schema = FeedbackRequestSchema()
feedback_response_schema = FeedbackResponseSchema()
