from flask import Blueprint, jsonify
from sqlalchemy.sql.expression import func
from webargs.flaskparser import use_kwargs

from prephouse.models import Question
from prephouse.schemas.question_schema import (
    question_request_schema,
    question_response_schema,
)

question_api = Blueprint("question_api", __name__, url_prefix="/question")


@question_api.get("/")
@use_kwargs(question_request_schema, location="query")
def get_question(question_categories, limit, randomize):
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
