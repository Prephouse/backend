from flask import Blueprint, request

from prephouse.api.decorators import check_token

# Might not need this endpoint because of firebase

signin_api = Blueprint("signin_api", __name__, url_prefix="/signin")


@signin_api.post("/")
@check_token
def signin():
    return {"firebase_id": request.user.id}
