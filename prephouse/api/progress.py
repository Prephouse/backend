from collections import defaultdict

from flask import Blueprint, jsonify, request
from sqlalchemy import asc, desc, func
from webargs.flaskparser import use_kwargs

from prephouse.decorators.authentication import private_route
from prephouse.models import Feedback, Upload, UploadQuestion
from prephouse.schemas.progress_schema import (
    category_scores_response_schema,
    progress_request_schema,
    progress_response_schema,
    session_scores_request_schema,
    session_scores_response_schema,
)

progress_api = Blueprint("progress", __name__, url_prefix="/progress")


@progress_api.get("scores_per_category/")
@use_kwargs(session_scores_request_schema, location="query")
@private_route
def get_scores_per_feature_across_all_sessions():
    """
    Get all the scores for a user per session, categorized by the feature.

    User >> Uploads >> Upload Questions >> Feedback
    """
    user_id = request.user.id
    res = defaultdict(list)

    for upload in Upload.query.filter_by(user_id=user_id).order_by(asc(Upload.date_uploaded)):
        res["dates"].append(upload.date_uploaded)
        res["overall_scores"].append(float(upload.score or 0))
        session_scores = {f.get_api_safe_feature_name(): 0 for f in Feedback.FeedbackCategory}

        query = (
            Upload.query.join(UploadQuestion, UploadQuestion.upload_id == Upload.id)
            .join(Feedback, Feedback.uq_id == UploadQuestion.id)
            .filter(
                Upload.id == upload.id,
                UploadQuestion.upload_id == upload.id,
                Feedback.subcategory == "score",
            )
            .add_columns(
                Upload.id,
                Feedback.category,
                func.avg(Feedback.result).label("avg_score"),
            )
            .group_by(Upload.id, Feedback.category)
            .all()
        )

        for q in query:
            session_scores[q.category.get_api_safe_feature_name()] = q.avg_score

        for feature, score in session_scores.items():
            res[f"{feature}_scores"].append(float(score))

    return jsonify(category_scores_response_schema.dump(res))


@progress_api.get("scores_per_session/")
@use_kwargs(session_scores_request_schema, location="query")
@private_route
def get_scores_per_session():
    """
    Get scores of all features for each session the user has.

    User >> Uploads >> Upload Questions >> Feedback
    """
    scores_dict = defaultdict(lambda: [None, None, 0, {f: 0 for f in Feedback.FeedbackCategory}])
    res = []
    user_id = request.user.id

    query = (
        Upload.query.join(UploadQuestion, UploadQuestion.upload_id == Upload.id, isouter=True)
        .join(Feedback, Feedback.uq_id == UploadQuestion.id, isouter=True)
        .filter(Upload.user_id == user_id)
        .group_by(Upload.id, Feedback.category)
        .order_by(desc(Upload.date_uploaded))
        .add_columns(
            Upload.id,
            Upload.date_uploaded,
            Upload.score.label("upload_score"),
            Upload.category.label("upload_category"),
            Feedback.category.label("feedback_category"),
            func.avg(Feedback.result).label("avg_score"),
        )
    ).all()

    for feedback in query:
        scores_dict[feedback.id][0] = feedback.date_uploaded
        scores_dict[feedback.id][1] = feedback.upload_category
        scores_dict[feedback.id][2] = feedback.upload_score
        scores_dict[feedback.id][3][feedback.feedback_category] = float(feedback.avg_score or 0)

    for upload_id, (date, upload_category, upload_score, scores) in scores_dict.items():
        item = {
            f"{f.get_api_safe_feature_name()}_score": scores[f] for f in Feedback.FeedbackCategory
        }
        item |= {
            "date": date,
            "session_category": upload_category.get_category_name(),
            "session_id": upload_id,
            "overall_score": upload_score,
        }
        res.append(item)

    return jsonify(session_scores_response_schema.dump({"sessions": res}))


@progress_api.get("feature_per_question/")
@use_kwargs(progress_request_schema, location="query")
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
    return jsonify(progress_response_schema.dump(res))


@progress_api.get("feature_per_session/")
@use_kwargs(progress_request_schema, location="query")
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
    return jsonify(progress_response_schema.dump(res))


@progress_api.get("overall_per_session/")
@use_kwargs(progress_request_schema, location="query")
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
    return jsonify(progress_response_schema.dump(res))
