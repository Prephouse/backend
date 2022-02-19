from collections import defaultdict

from flask import Blueprint, jsonify, request
from sqlalchemy.sql.expression import func
from webargs.flaskparser import abort, use_kwargs

from prephouse.decorators.authentication import private_route
from prephouse.models import Question, Upload
from prephouse.schemas.question_schema import (
    question_request_schema,
    question_response_schema,
    question_upload_request_schema,
    question_upload_response_schema,
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


@question_api.get("<upload_id>/")
@use_kwargs(question_upload_request_schema, location="query")
@private_route
def get_questions_for_upload(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    if upload is None or upload.user_id != request.user.id:
        abort(401)

    query = Upload.query.filter_by(id=upload_id)
    response = {
        "upload_id": upload_id,
        "questions": defaultdict(dict),
    }
    if upload := query.first():
        for question in upload.questions:
            response["questions"][question.id] = {
                "category": question.category,
                "category_name": question.category.get_category_name(),
                "question": question.question,
                "description": question.description,
            }

    return jsonify(question_upload_response_schema.dump(response))
