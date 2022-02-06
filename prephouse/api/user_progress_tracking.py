from flask import Blueprint, abort, jsonify, request

from prephouse.api.decorators import check_token
from prephouse.models import Feedback, Upload, UploadQuestion
from prephouse.schemas.user_progress_tracking_schema import (
    user_progress_tracking_request,
    user_progress_tracking_response,
)
user_progress_tracking_api = Blueprint(
    "user_progress_tracking", __name__, url_prefix="/user_progress_tracking"
)

@user_progress_tracking_api.get("/feature_per_question")
@check_token
def get_score_per_feature_per_question():
    if validation_errors := user_progress_tracking_request.validate(request.args):
        abort(422, validation_errors)
    question_id = request.args.get("question_id")
    # feature_scores = dict.fromkeys(Feedback.FeedbackCategory, 0.0)

    query = UploadQuestion.query
    if question_id:
        query = query.filter(question_id=UploadQuestion.upload_id)

    # query all feedbacks of one question in a session
    response = []
    for feature in Feedback.FeedbackCategory:
        query = query.join(Feedback).add_columns(
            UploadQuestion.upload_id,
            Feedback.id,
            Feedback.category,
            Feedback.result,
        )
        query = query.filter_by(category=feature)
        feedback = query.first()
        # feature_scores[feature] = float(feedback.result)

        item = {
            "id": feedback.id,
            "score": float(feedback.result),
        }
        response.append(item)
    return jsonify(user_progress_tracking_response.dump(response))


@user_progress_tracking_api.get("/feature_per_session")
@check_token
def get_overall_score_per_feature_per_session():
    # feature_scores = dict.fromkeys(Feedback.FeedbackCategory, 0.0)
    if validation_errors := user_progress_tracking_request.validate(request.args):
        abort(422, validation_errors)
    session_id = request.args.get("session_id")

    # query all feedbacks of all questions in a session
    query = Upload.query.filter_by(upload_id=session_id)
    query = (
        query.join(UploadQuestion)
        .join(Feedback)
        .add_columns(
            Upload.id,
            Feedback.category,
            Feedback.subcategory,
            Feedback.result,
        )
    )

    response = []
    feedbacks = query.filter_by(subcategory="score")
    for feedback in feedbacks or []:
        # feature_scores[feedback.category] += float(feedback.result)
        item = {
            "id": feedback.id,
            "score": float(feedback.result),
        }
        response.append(item)
    return jsonify(user_progress_tracking_response.dump(response))


@user_progress_tracking_api.get("/overall_session")
@check_token
def get_overall_score_per_all_feature_per_session():
    if validation_errors := user_progress_tracking_request.validate(request.args):
        abort(422, validation_errors)
    session_id = request.args.get("session_id")
    feature_scores = dict.fromkeys(Feedback.FeedbackCategory, 0.0)

    # query all feedbacks of all questions in a session
    query = Upload.query.filter_by(upload_id=session_id)
    query = (
        query.join(UploadQuestion)
        .join(Feedback)
        .add_columns(
            Upload.id,
            Feedback.category,
            Feedback.subcategory,
            Feedback.result,
        )
    )

    response = []
    feedbacks = query.filter_by(subcategory="score")
    for feature in Feedback.FeedbackCategory:
        query = query.filter_by(category=feature)
        for feedback in feedbacks or []:
            feature_scores[feature] += float(feedback.result)

        item = {
            "id": feedback.id,
            "score": feature_scores[feature] / len(feedbacks),
        }
        response.append(item)
    return jsonify(user_progress_tracking_response.dump(response))
