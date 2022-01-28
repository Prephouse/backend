from firebase_admin import auth
from flask import Blueprint, request

from prephouse.models import User

# Might not need this endpoint because of firebase

signup_api = Blueprint("signup_api", __name__, url_prefix="/signup")


@signup_api.post("/")
def signup():
    email = request.form.get("email", type=str)
    password = request.form.get("password", type=str)
    first_name = request.form.get("first_name", type=str)
    last_name = request.form.get("last_name", type=str)

    # TODO Transaction the two steps below

    firebase_user = auth.create_user(
        email=email, password=password, display_name=f"{first_name} {last_name}"
    )
    app_user = User(first_name=first_name, last_name=last_name, email=email, id=firebase_user.uid)

    return {"firebase_id": app_user.id}
