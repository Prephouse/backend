from flask import Blueprint, jsonify, request
from psycopg2.extras import NumericRange
from sqlalchemy import desc
from webargs.flaskparser import use_kwargs

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


@feedback_api.get("/")
@use_kwargs(upload_request_schema, location="query")
@private_route
def get_uploads(page):
    upload_page = (
        Upload.query.filter_by(user_id=request.user.id)
        .order_by(desc(Upload.date_uploaded))
        .paginate(page=page, per_page=20, error_out=False)
    )
    response = {
        "page": upload_page.next_num,
        "has_next": upload_page.has_next,
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


@feedback_api.get("<upload_id>/")
@use_kwargs(feedback_request_schema, location="query")
@private_route
def get_feedback(time_start, time_end, category, upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    if upload is None or upload.user_id != request.user.id:
        return {"Unauthorized access"}, 401

    query = UploadQuestion.query
    query = query.filter_by(upload_id=upload_id)
    query = query.join(Feedback).add_columns(
        UploadQuestion.upload_id,
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

    response = []
    feedbacks: list[UploadQuestion | Feedback] = query.all() or []
    for feedback in feedbacks:
        item = {
            "id": feedback.id,
            "upload_id": feedback.upload_id,
            "subcategory": feedback.subcategory,
            "category": feedback.category,
            "comment": feedback.comment,
            "result": float(feedback.result),
        }
        if tr := feedback.time_range:
            time_start, time_end = get_integral_numeric_range_bounds(tr)
            item |= {
                "time_start": time_start,
                "time_end": time_end,
            }
        response.append(item)

    return jsonify(feedback_response_schema.dump(response))
