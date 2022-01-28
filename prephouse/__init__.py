from flask import Blueprint

from prephouse.app_factory import create_app
from prephouse.models import db

app = create_app(db)

from prephouse.api.analyze import analyze_api  # noqa: E402
from prephouse.api.feedback import feedback_api  # noqa: E402
from prephouse.api.signin import signin_api  # noqa: E402
from prephouse.api.signup import signup_api  # noqa: E402
from prephouse.interceptors.firebase_interceptor import (  # noqa: E402
    firebase_interceptor,
)
from prephouse.interceptors.rollbar_interceptor import rollbar_interceptor  # noqa: E402

blueprints: tuple[Blueprint, ...] = (
    firebase_interceptor,
    rollbar_interceptor,
    feedback_api,
    analyze_api,
    signup_api,
    signin_api,
)
for blueprint in blueprints:
    app.register_blueprint(blueprint)
