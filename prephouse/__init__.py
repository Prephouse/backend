from flask import Blueprint

from prephouse.app_factory import create_app
from prephouse.models import db

app = create_app(db)

import prephouse.errorhandlers.http_error_handler  # noqa: E402
import prephouse.errorhandlers.validation_error_handler  # noqa: E402
import prephouse.interceptors.firebase_interceptor  # noqa: E402
import prephouse.interceptors.rollbar_interceptor  # noqa: E402, F401
from prephouse.api.analyze import analyze_api  # noqa: E402
from prephouse.api.feedback import feedback_api  # noqa: E402
from prephouse.api.leaderboard import leaderboard_api  # noqa: E402
from prephouse.api.progress import progress_api  # noqa: E402
from prephouse.api.question import question_api  # noqa: E402
from prephouse.api.upload import upload_api  # noqa: E402

blueprints: tuple[Blueprint, ...] = (
    feedback_api,
    analyze_api,
    question_api,
    progress_api,
    leaderboard_api,
    upload_api,
)
for blueprint in blueprints:
    app.register_blueprint(blueprint)
