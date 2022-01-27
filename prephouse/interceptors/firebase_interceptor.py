import firebase_admin
from flask import Blueprint, current_app

firebase_interceptor = Blueprint("firebase_interceptor", __name__)


@current_app.before_first_request
def init_firebase():
    firebase_admin.initialize_app()
