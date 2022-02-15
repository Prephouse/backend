from flask import Blueprint

from prephouse.app_factory import create_app
from prephouse.models import db

app = create_app(db)

from prephouse.api.analyze import analyze_api  # noqa: E402
from prephouse.api.cross_user_perf_tracking import cross_user_perf_tracking_api
from prephouse.api.feedback import feedback_api  # noqa: E402
from prephouse.api.question import question_api  # noqa: E402
from prephouse.api.user_progress_tracking import (  # noqa: E402
    user_progress_tracking_api,
)
from prephouse.interceptors.firebase_interceptor import (  # noqa: E402
    firebase_interceptor,
)
from prephouse.interceptors.rollbar_interceptor import rollbar_interceptor  # noqa: E402

blueprints: tuple[Blueprint, ...] = (
    firebase_interceptor,
    rollbar_interceptor,
    feedback_api,
    analyze_api,
    question_api,
    user_progress_tracking_api,
    cross_user_perf_tracking_api,
)
for blueprint in blueprints:
    app.register_blueprint(blueprint)
