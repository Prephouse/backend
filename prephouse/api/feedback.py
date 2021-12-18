from flask import Blueprint, abort, jsonify, request
from psycopg2.extras import NumericRange

from prephouse.base_response import BaseResponse
from prephouse.models import Feedback
from prephouse.schemas.feedback_schema import FeedbackSchema
from prephouse.utils import constants
from prephouse.utils.sql_utils import get_integral_numeric_range_bounds

feedback_api = Blueprint("feedback_api", __name__, url_prefix="/feedback")


# TODO integrate OAuth check
@feedback_api.get("/")
def get_feedback() -> BaseResponse[FeedbackSchema]:
    upload_ids = request.args.getlist("upload_ids")
    time_start = request.args.get("time_start", type=int, default=0)
    time_end = request.args.get("time_end", type=int, default=constants.PSQL_INT_MAX)
    category = request.args.get("category", type=int)

    query = Feedback.query
    if upload_ids:
        query = query.filter(Feedback.upload_id.in_(upload_ids))
    if category is not None:
        try:
            category = Feedback.Feature(category)
        except ValueError:
            abort(400)
        query = query.filter_by(type=category)
    query = query.filter(
        Feedback.time_range is not None
        and Feedback.time_range.contained_by(NumericRange(time_start, time_end))
    )

    response: FeedbackSchema = []
    for feedback in query.all() or []:
        item = {
            "id": feedback.id,
            "upload_id": feedback.upload_id,
            "category": feedback.category.value,
            "comment": feedback.comment,
            "score": float(feedback.score),
        }
        if tr := feedback.time_range:
            time_start, time_end = get_integral_numeric_range_bounds(tr)
            item |= {
                "time_start": time_start,
                "time_end": time_end,
            }
        response.append(item)

    return jsonify(response)
