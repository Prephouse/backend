from flask import Blueprint, abort, jsonify, request
from psycopg2.extras import NumericRange

from prephouse.models import Feedback
from prephouse.schemas.feedback_schema import (
    feedback_request_schema,
    feedback_response_schema,
)
from prephouse.utils import constants
from prephouse.utils.sql_utils import get_integral_numeric_range_bounds

feedback_api = Blueprint("feedback_api", __name__, url_prefix="/feedback")


# TODO integrate OAuth check
@feedback_api.get("/")
def get_feedback():
    if validation_errors := feedback_request_schema.validate(request.args):
        abort(422, validation_errors)
    upload_ids = request.args.getlist("upload_ids")
    time_start = request.args.get("time_start", type=int, default=0)
    time_end = request.args.get("time_end", type=int, default=constants.PSQL_INT_MAX)
    category = request.args.get("category", type=int)

    query = Feedback.query
    if upload_ids:
        query = query.filter(Feedback.upload_id.in_(upload_ids))
    if category is not None:
        query = query.filter_by(category=Feedback.Feature(category))
    query = query.filter(
        Feedback.time_range is not None
        and Feedback.time_range.contained_by(NumericRange(time_start, time_end))
    )

    response = []
    for feedback in query.all() or []:
        item = {
            "id": feedback.id,
            "upload_id": feedback.upload_id,
            "subcategory": feedback.subcategory,
            "category": feedback.category.value,
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
