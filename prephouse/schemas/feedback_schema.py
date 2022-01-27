from marshmallow import Schema, fields, validate

from prephouse.models import Feedback
from prephouse.utils import constants


class FeedbackRequestSchema(Schema):
    upload_ids = fields.List(fields.Int, dump_default=None)
    time_start = fields.Int(dump_default=0)
    time_end = fields.Int(dump_default=constants.PSQL_INT_MAX)
    category = fields.Int(validate=validate.OneOf(list(map(int, Feedback.FeedbackCategory))))


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


feedback_request_schema = FeedbackRequestSchema()
feedback_response_schema = FeedbackResponseSchema(many=True)
