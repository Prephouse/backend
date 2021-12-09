import os

import rollbar
import rollbar.contrib.flask
from flask import Blueprint, got_request_exception

from api.analyze import analyze_api
from api.feedback import feedback_api
from create_app import create_app
from database import db

app = create_app(db)


@app.before_first_request
def init_rollbar():
    rollbar.init(
        os.environ["ROLLBAR_ACCESS_TOKEN"],
        environment=os.environ["FLASK_ENV"],
        root=os.path.dirname(os.path.realpath(__file__)),
        allow_logging_basic_config=False,
    )
    # send exceptions from `app` to rollbar, using flask's signal system
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


blueprints: tuple[Blueprint, ...] = (
    feedback_api,
    analyze_api,
)
for blueprint in blueprints:
    app.register_blueprint(blueprint)


if __name__ == "__main__":
    app.run()
