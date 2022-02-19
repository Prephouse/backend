from flask import current_app
from werkzeug.exceptions import BadRequest, Unauthorized, UnprocessableEntity


@current_app.errorhandler(Unauthorized)
@current_app.errorhandler(UnprocessableEntity)
@current_app.errorhandler(BadRequest)
def handle_http_error(err):
    headers = err.data.get("headers", None)
    if err.code == Unauthorized.code:
        messages = str(err)
    else:
        messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return {"errors": messages}, err.code, headers
    else:
        return {"errors": messages}, err.code
