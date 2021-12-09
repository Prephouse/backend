from flask import Blueprint, abort, jsonify, request
from psycopg2.extras import NumericRange

from prephouse.model import Feedback
from prephouse.utils import constants
from prephouse.utils.sql_utils import get_integral_numeric_range_bounds

feedback_api = Blueprint("feedback_api", __name__, url_prefix="/feedback")


# TODO integrate OAuth check
@feedback_api.route("/")
def get_feedback():
    upload_ids = request.args.getlist("upload_ids")
    time_start = request.args.get("time_start", type=int, default=0)
    time_end = request.args.get("time_end", type=int, default=constants.PSQL_INT_MAX)
    feedback_type = request.args.get("feedback_type", type=int)

    query = Feedback.query
    if upload_ids:
        query = query.filter(Feedback.upload_id.in_(upload_ids))
    if feedback_type is not None:
        try:
            feedback_type = Feedback.Type(feedback_type)
        except ValueError:
            abort(400)
        query = query.filter_by(type=feedback_type)
    query = query.filter(Feedback.time_range.contained_by(NumericRange(time_start, time_end)))

    response = []
    for feedback in query.all() or []:
        time_start, time_end = get_integral_numeric_range_bounds(feedback.time_range)
        response.append(
            {
                "id": feedback.id,
                "upload_id": feedback.upload_id,
                "type": feedback.type.value,
                "text": feedback.text,
                "score": float(feedback.score),
                "time_start": time_start,
                "time_end": time_end,
            }
        )

    return jsonify(response)
