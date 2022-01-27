from flask import Blueprint

from prephouse.app_factory import create_app
from prephouse.models import db

app = create_app(db)

from prephouse.api.analyze import analyze_api  # noqa: E402
from prephouse.api.feedback import feedback_api  # noqa: E402
from prephouse.interceptors.rollbar_interceptor import rollbar_interceptor  # noqa: E402


import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate() # Have the path stored as an environment variable for use in call to Certificate when ready
firebase_admin.initialize_app(cred)

blueprints: tuple[Blueprint, ...] = (
    rollbar_interceptor,
    feedback_api,
    analyze_api,
)
for blueprint in blueprints:
    app.register_blueprint(blueprint)
