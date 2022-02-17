from flask import Blueprint, jsonify, request
from sqlalchemy import desc
from webargs.flaskparser import use_kwargs

from prephouse.decorators.authentication import private_route
from prephouse.models import Upload
from prephouse.schemas.cross_user_perf_tracking_schema import (
    user_perf_tracking_overall_scores_request,
    user_perf_tracking_overall_scores_response,
)

cross_user_perf_tracking_api = Blueprint(
    "cross_user_perf_tracking", __name__, url_prefix="/cross_user_perf_tracking"
)


@cross_user_perf_tracking_api.get("compare_overall_outputs/")
@use_kwargs(user_perf_tracking_overall_scores_request, location="query")
@private_route
def get_overall_score_comparison_data():
    """Get a comparison of a user's score relative to their past performance and to other users."""
    # Match on user_id, disregard results with null for overall score (Upload.score) value
    user_id = request.user.id
    query = (
        Upload.query.filter(Upload.score is not None, Upload.user_id == user_id)
        .order_by(desc(Upload.date_uploaded))
        .all()
    )
    latest_overall_score = query[0].score if len(query) > 0 else 0
    all_user_overall_score_data = query

    cross_user_query = Upload.query.filter(
        Upload.score is not None, Upload.user_id != user_id
    ).all()
    cross_user_query_scores = [upload.score for upload in cross_user_query]
    average_all_overall_score_all_users = (
        sum(cross_user_query_scores) / len(cross_user_query_scores)
        if len(cross_user_query_scores)
        else 0
    )

    item = {
        "latest_overall_score": latest_overall_score,
        "overall_scores_history_current_user": [
            upload.score for upload in all_user_overall_score_data
        ],
        "overall_scores_history_all_other_users": cross_user_query_scores,
        "average_overall_scores_history_all_other_users": average_all_overall_score_all_users,
    }

    return jsonify(user_perf_tracking_overall_scores_response.dump(item))
