from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from prephouse.decorators.authentication import private_route
from prephouse.models import Feedback, Upload, UploadQuestion
from prephouse.schemas.user_progress_tracking_schema import (
    user_progress_tracking_request,
    user_progress_tracking_response,
)

user_progress_tracking_api = Blueprint(
    "user_progress_tracking", __name__, url_prefix="/user_progress_tracking"
)


@user_progress_tracking_api.get("feature_per_question/")
@use_kwargs(user_progress_tracking_request, location="query")
@private_route
def get_score_per_feature_per_question_per_session(session_id):
    """
    Get the score for all features for all questions for a given session.

    Session >> Question >> Feature Score
    """
    upload_questions = UploadQuestion.query.filter_by(upload_id=session_id)
    scores = [
        (feedback.category.name, float(feedback.result), upload_question.question_id)
        for upload_question in upload_questions
        for feedback in upload_question.feedbacks
    ]

    res = {"session_id": session_id, "response_data": scores}
    return jsonify(user_progress_tracking_response.dump(res))


@user_progress_tracking_api.get("feature_per_session/")
@use_kwargs(user_progress_tracking_request, location="query")
@private_route
def get_score_per_feature_per_session(session_id):
    """
    Get the total score for each feature for a given session.

    Session >> Feature Score
    """
    upload_questions = UploadQuestion.query.filter_by(upload_id=session_id)
    scores = [
        (feedback.category.name, float(feedback.result), upload_question.question_id)
        for upload_question in upload_questions
        for feedback in upload_question.feedbacks
    ]

    feature_scores_dict = {}
    for feature_name in Feedback.FeedbackCategory:
        feature_scores_dict[feature_name.name] = 0
    for score_data in scores:
        feature_scores_dict[score_data[0]] += score_data[1]

    res = {"session_id": session_id, "response_data": feature_scores_dict}
    return jsonify(user_progress_tracking_response.dump(res))


@user_progress_tracking_api.get("overall_per_session/")
@use_kwargs(user_progress_tracking_request, location="query")
@private_route
def get_overall_score_per_session(session_id):
    """
    Get the overall score for a given session.

    Session >> Overall Score
    """
    query = Upload.query.filter_by(id=session_id)
    response = query.first()

    res = {
        "session_id": session_id,
        "response_data": response.score if response else -1,
    }
    return jsonify(user_progress_tracking_response.dump(res))
