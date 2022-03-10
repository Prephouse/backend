from collections import defaultdict

from flask import Blueprint, jsonify, request
from psycopg2.extras import NumericRange
from sqlalchemy import desc
from webargs.flaskparser import abort, use_kwargs

from prephouse.decorators.authentication import private_route
from prephouse.models import Feedback, Upload, UploadQuestion
from prephouse.schemas.feedback_schema import (
    feedback_request_schema,
    feedback_response_schema,
    upload_request_schema,
    upload_response_schema,
)
from prephouse.utils.sql_utils import get_integral_numeric_range_bounds

feedback_api = Blueprint("feedback_api", __name__, url_prefix="/feedback")


@feedback_api.get("")
@use_kwargs(upload_request_schema, location="query")
@private_route
def get_uploads(page, per_page):
    upload_page = (
        Upload.query.filter_by(user_id=request.user.id)
        .order_by(desc(Upload.date_uploaded))
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    response = {
        "next_page": upload_page.next_num,
        "has_next": upload_page.has_next,
        "total_pages": upload_page.pages,
        "uploads": [
            {
                "id": upload.id,
                "category": upload.category,
                "date_uploaded": upload.date_uploaded,
                "score": upload.score,
            }
            for upload in upload_page.items or []
        ],
    }

    return jsonify(upload_response_schema.dump(response))


@feedback_api.get("<upload_id>")
@use_kwargs(feedback_request_schema, location="query")
@private_route
def get_feedback(time_start, time_end, category, upload_id):
    upload = Upload.query.get(upload_id)
    if upload is None or upload.user_id != request.user.id:
        abort(401)

    query = UploadQuestion.query.filter_by(upload_id=upload_id)
    query = query.join(Feedback).add_columns(
        UploadQuestion.upload_id,
        UploadQuestion.question_id,
        Feedback.id,
        Feedback.category,
        Feedback.subcategory,
        Feedback.comment,
        Feedback.result,
        Feedback.confidence,
        Feedback.time_range,
    )
    if category is not None:
        query = query.filter_by(category=Feedback.FeedbackCategory(category))
    query = query.filter(
        Feedback.time_range is not None
        and Feedback.time_range.contained_by(NumericRange(time_start, time_end))
    )

    response = {
        "upload_id": upload_id,
        "feedbacks": defaultdict(dict),
    }
    for feedback in query.all() or []:
        item = {
            "id": feedback.id,
            "feature_name": feedback.category.get_feature_name(),
            "subcategory": feedback.subcategory,
            "comment": feedback.comment,
            "result": feedback.result,
        }
        if tr := feedback.time_range:
            time_start, time_end = get_integral_numeric_range_bounds(tr)
            item |= {
                "time_start": time_start,
                "time_end": time_end,
            }
        response["feedbacks"][feedback.question_id][feedback.category] = item

    return jsonify(feedback_response_schema.dump(response))
