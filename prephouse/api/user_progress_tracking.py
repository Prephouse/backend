from flask import Blueprint, abort, jsonify, request

from prephouse.decorators.authentication import private_route
from prephouse.models import Feedback, Upload, UploadQuestion
from prephouse.schemas.user_progress_tracking_schema import (
    user_progress_tracking_question_request,
    user_progress_tracking_response,
    user_progress_tracking_session_request,
)

user_progress_tracking_api = Blueprint(
    "user_progress_tracking", __name__, url_prefix="/user_progress_tracking"
)


@user_progress_tracking_api.get("feature_per_question/")
@private_route
def get_score_per_feature_per_question():
    if validation_errors := user_progress_tracking_question_request.validate(request.args):
        abort(422, validation_errors)
    question_id = request.args.get("question_id")

    query = UploadQuestion.query
    if question_id:
        query = query.filter_by(question_id=question_id)

    # query all feedbacks of one question in a session
    response = []
    query = query.join(Feedback).add_columns(
        Feedback.id,
        Feedback.category,
        Feedback.result,
    )

    for feature in Feedback.FeedbackCategory:
        sub_query = query.filter_by(category=feature, subcategory="score")
        feedback = sub_query.first()

        if feedback:
            item = {
                "id": feedback.id,
                "score": float(feedback.result),
            }
            response.append(item)
    return jsonify(user_progress_tracking_response.dump(response))


@user_progress_tracking_api.get("feature_per_session/")
@private_route
def get_overall_score_per_feature_per_session():
    if validation_errors := user_progress_tracking_session_request.validate(request.args):
        abort(422, validation_errors)
    session_id = request.args.get("session_id")

    # query all feedbacks of all questions in a session
    query = Upload.query.filter_by(id=session_id)
    query = (
        query.join(UploadQuestion, Upload.id == UploadQuestion.upload_id)
        .join(Feedback, UploadQuestion.id == Feedback.uq_id)
        .add_columns(
            Feedback.id,
            Feedback.category,
            Feedback.subcategory,
            Feedback.result,
        )
    )

    response = []
    feedbacks = query.filter_by(subcategory="score")

    for feedback in feedbacks.all() or []:
        # feature_scores[feedback.category] += float(feedback.result)
        item = {
            "id": feedback.id,
            "score": float(feedback.result),
        }
        response.append(item)
    return jsonify(user_progress_tracking_response.dump(response))


@user_progress_tracking_api.get("overall_session/")
@private_route
def get_overall_score_per_all_feature_per_session():
    if validation_errors := user_progress_tracking_session_request.validate(request.args):
        abort(422, validation_errors)
    session_id = request.args.get("session_id")
    feature_scores = dict.fromkeys(Feedback.FeedbackCategory, 0.0)

    # query all feedbacks of all questions in a session
    query = Upload.query.filter_by(id=session_id)
    query = (
        query.join(UploadQuestion, Upload.id == UploadQuestion.upload_id)
        .join(Feedback, UploadQuestion.id == Feedback.uq_id)
        .add_columns(
            Upload.id,
            Feedback.category,
            Feedback.subcategory,
            Feedback.result,
        )
    )

    response = []
    query = query.filter_by(subcategory="score")
    for feature in Feedback.FeedbackCategory:
        feedbacks = query.filter_by(category=feature).all()
        for feedback in feedbacks or []:
            feature_scores[feature] += float(feedback.result)

        if feedbacks:
            item = {
                "id": session_id,
                "score": feature_scores[feature] / len(feedbacks),
            }
            response.append(item)
    return jsonify(user_progress_tracking_response.dump(response))
