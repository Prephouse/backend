from flask import current_app
from werkzeug.exceptions import BadRequest, UnprocessableEntity


@current_app.errorhandler(UnprocessableEntity)
@current_app.errorhandler(BadRequest)
def handle_http_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return {"errors": messages}, err.code, headers
    else:
        return {"errors": messages}, err.code
