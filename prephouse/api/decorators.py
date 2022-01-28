from functools import wraps

from firebase_admin import auth
from flask import request

from prephouse.models import User


def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.headers.get("Authorization"):
            return {"message": "No token provided"}, 400
        try:
            id_token = request.headers["Authorization"].split(" ").pop()
            firebase_user = auth.verify_id_token(id_token)

            app_user = User.query.filter(id=firebase_user.uid).first()

            if not app_user:
                app_user = User(
                    first_name=firebase_user.display_name,
                    last_name="",
                    email=firebase_user.email,
                    id=firebase_user.uid,
                )

            request.user = app_user
        except Exception:
            return {"message": "Invalid token provided."}, 400
        return f(*args, **kwargs)

    return wrap
