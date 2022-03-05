from marshmallow import Schema
from webargs import fields


class NewQuestionUploadIdResponseSchema(Schema):
    id = fields.UUID(required=True)


new_question_upload_id_response_schema = NewQuestionUploadIdResponseSchema()
