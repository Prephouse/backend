from flask import Blueprint, abort, jsonify, request
from sqlalchemy.sql.expression import func

from prephouse.models import Question
from prephouse.schemas.question_schema import (
    question_request_schema,
    question_response_schema,
)

question_api = Blueprint("question_api", __name__, url_prefix="/question")


@question_api.get("/")
def get_question():
    if validation_errors := question_request_schema.validate(request.args):
        abort(422, validation_errors)
    question_categories = request.args.getlist("question_categories")
    limit = request.args.get("limit", type=int)
    randomize = request.args.get("randomize", type=bool)

    query = Question.query
    if question_categories is not None:
        query = query.filter_by(Question.QuestionCategory.in_(question_categories))
    if randomize:
        query = query.order_by(func.random())
    if limit:
        query = query.limit(limit)

    response = []
    questions: list[Question] = query.all() or []
    for question in questions:
        response.append(
            {
                "id": question.id,
                "category": question.category,
                "question": question.question,
                "description": question.description,
                "sample_answer": question.sample_answer,
                "frequency": question.frequency,
            }
        )

    return jsonify(question_response_schema.dump(response))
