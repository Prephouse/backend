from flask import Blueprint

from prephouse.app_factory import create_app
from prephouse.models import db

app = create_app(db)

from prephouse.api.analyze import analyze_api  # noqa: E402
from prephouse.api.feedback import feedback_api  # noqa: E402
from prephouse.watchers.rollbar_watcher import rollbar_watcher  # noqa: E402

blueprints: tuple[Blueprint, ...] = (
    rollbar_watcher,
    feedback_api,
    analyze_api,
)
for blueprint in blueprints:
    app.register_blueprint(blueprint)
