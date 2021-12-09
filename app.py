from flask import Blueprint

from create_app import create_app
from model import db

app = create_app(db)

from api.analyze import analyze_api  # noqa: E402
from api.feedback import feedback_api  # noqa: E402
from watchers.rollbar_watcher import rollbar_watcher  # noqa: E402

blueprints: tuple[Blueprint, ...] = (
    rollbar_watcher,
    feedback_api,
    analyze_api,
)
for blueprint in blueprints:
    app.register_blueprint(blueprint)


if __name__ == "__main__":
    app.run()
