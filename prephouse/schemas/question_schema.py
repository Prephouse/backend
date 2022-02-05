from marshmallow import Schema, fields, validate

from prephouse.models import Question


class QuestionRequestSchema(Schema):
    question_categories = fields.List(
        fields.Int(
            required=True, validate=validate.OneOf(list(map(int, Question.QuestionCategory)))
        ),
        dump_default=None,
    )
    limit = fields.Int(dump_default=0)
    randomize = fields.Bool(dump_default=False)


class QuestionResponseSchema(Schema):
    id = fields.Int(required=True)
    category = fields.Int(
        required=True, validate=validate.OneOf(list(map(int, Question.QuestionCategory)))
    )
    question = fields.Str()
    description = fields.Str()
    sample_answer = fields.Str()
    frequency = fields.Int()


question_request_schema = QuestionRequestSchema()
question_response_schema = QuestionResponseSchema(many=True)