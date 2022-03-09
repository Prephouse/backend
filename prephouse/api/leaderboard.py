from flask import Blueprint, jsonify, request
from sqlalchemy import desc, func
from sqlalchemy.orm import load_only
from webargs.flaskparser import use_kwargs

from prephouse.decorators.authentication import private_route
from prephouse.models import Engine, Upload, User
from prephouse.schemas.leaderboard_schema import (
    leaderboard_overview_request_schema,
    leaderboard_overview_response_schema,
    leaderboard_request_schema,
    leaderboard_response_schema,
)

leaderboard_api = Blueprint("leaderboard_api", __name__, url_prefix="/leaderboard")


@leaderboard_api.get("/")
@use_kwargs(leaderboard_request_schema, location="query")
def get_leaderboard(page, per_page):
    upload_page = (
        Upload.query.join(Engine, Engine.id == Upload.engine_id)
        .join(User, User.id == Upload.user_id)
        .add_columns(
            Engine.configuration,
            Engine.version,
            User.name,
            Upload.id,
            Upload.category,
            Upload.date_uploaded,
            Upload.score,
        )
        .filter(Upload.score is not None)
        .order_by(desc(Upload.score))
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    response = {
        "next_page": upload_page.next_num,
        "has_next": upload_page.has_next,
        "total_pages": upload_page.pages,
        "uploads": [
            {
                "standing": idx + 1,
                "session_id": upload.id,
                "username": upload.name,
                "category": upload.category,
                "category_name": upload.category.get_category_name(),
                "date_uploaded": upload.date_uploaded,
                "includes_video": True,
                "score": upload.score,
                "engine_version": upload.version,
            }
            for idx, upload in enumerate(upload_page.items or [])
        ],
    }

    return jsonify(leaderboard_response_schema.dump(response))


@leaderboard_api.get("overview/")
@use_kwargs(leaderboard_overview_request_schema, location="query")
@private_route
def get_leaderboard_overview():
    """Get a comparison of a user's score relative to their past performance and to other users."""
    user_id = request.user.id
    user_uploads = (
        Upload.query.options(load_only(Upload.score))
        .filter(Upload.score is not None, Upload.user_id == user_id)
        .order_by(desc(Upload.date_uploaded))
        .all()
    )
    user_scores = [u.score for u in (user_uploads or []) if u.score]

    global_upload_aggregates = (
        Upload.query.with_entities(func.avg(Upload.score).label("average_score"))
        .filter(Upload.score is not None)
        .all()
    )

    latest_overall_score = user_scores[0] if user_scores else None
    average_overall_score_user = sum(user_scores) / len(user_scores) if user_scores else None
    response = {
        "latest_overall_score": latest_overall_score,
        "average_overall_score_user": average_overall_score_user,
        "average_overall_score_global": global_upload_aggregates[0][0],
    }

    return jsonify(leaderboard_overview_response_schema.dump(response))
