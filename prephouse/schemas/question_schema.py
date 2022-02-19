from marshmallow import Schema
from webargs import fields, validate

from prephouse.models import Question


class QuestionRequestSchema(Schema):
    question_categories = fields.List(
        fields.Int(
            required=True,
            validate=validate.OneOf(list(map(int, Question.QuestionCategory))),
        ),
        missing=None,
    )
    limit = fields.Int(missing=0)
    randomize = fields.Bool(missing=False)


class QuestionResponseSchema(Schema):
    id = fields.Int(required=True)
    category = fields.Int(
        required=True,
        validate=validate.OneOf(list(map(int, Question.QuestionCategory))),
    )
    question = fields.Str()
    description = fields.Str()
    sample_answer = fields.Str()
    frequency = fields.Int()


class QuestionUploadRequestSchema(Schema):
    pass


class QuestionUploadResponseSchema(Schema):
    class SingleQuestion(QuestionResponseSchema):
        category_name = fields.Str(required=True)

    upload_id = fields.UUID(required=True)
    questions = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(SingleQuestion),
        required=True,
    )


question_request_schema = QuestionRequestSchema()
question_response_schema = QuestionResponseSchema(many=True)
question_upload_request_schema = QuestionUploadRequestSchema()
question_upload_response_schema = QuestionUploadResponseSchema()
