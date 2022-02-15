import json

from flask import Blueprint, abort, jsonify, request

from prephouse.decorators.authentication import private_route
from prephouse.models import Feedback, Upload, UploadQuestion
from prephouse.schemas.user_progress_tracking_schema import (
    user_progress_tracking_overall_score_session_response,
    user_progress_tracking_question_request,
    user_progress_tracking_question_response,
    user_progress_tracking_session_request,
    user_progress_tracking_session_response,
)

user_progress_tracking_api = Blueprint(
    "user_progress_tracking", __name__, url_prefix="/user_progress_tracking"
)

# The score for all features for all questions for all sessions
# Session >> Question >> Feature Score
@user_progress_tracking_api.get("feature_per_question/")
@private_route
def get_score_per_feature_per_question_per_session():
    if validation_errors := user_progress_tracking_question_request.validate(request.args):
        abort(422, validation_errors)
    session_id = request.args.get("session_id")

    upload_questions = UploadQuestion.query.filter_by(upload_id=session_id)
    scores = [
        (feedback.category.name, float(feedback.result), upload_question.question_id)
        for upload_question in upload_questions
        for feedback in upload_question.feedbacks
    ]

    return {"session_id": session_id, "response_data": json.dumps(scores)}


# Returns a total score for each feature for a given session
# Session >> Feature Score Averages
@user_progress_tracking_api.get("feature_per_session/")
@private_route
def get_score_per_feature_per_session():
    if validation_errors := user_progress_tracking_session_request.validate(request.args):
        abort(422, validation_errors)
    session_id = request.args.get("session_id")

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

    return {"session_id": session_id, "response_data": json.dumps(feature_scores_dict)}


# The overall score for all sessions
# Session >> Overall Score
@user_progress_tracking_api.get("overall_per_session/")
@private_route
def get_overall_score_per_session():
    if validation_errors := user_progress_tracking_session_request.validate(request.args):
        abort(422, validation_errors)
    session_id = request.args.get("session_id")

    query = Upload.query.filter_by(id=session_id)
    response = query.first()
    return {
        "session_id": session_id,
        "response_data": response.score if response else -1,
    }
