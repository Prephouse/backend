import firebase_admin
from flask import current_app


@current_app.before_first_request
def init_firebase():
    firebase_admin.initialize_app()
