import os

import rollbar
import rollbar.contrib.flask
from flask import Blueprint, current_app, got_request_exception

rollbar_watcher = Blueprint("rollbar_watcher", __name__)


@current_app.before_first_request
def init_rollbar():
    rollbar.init(
        os.environ["ROLLBAR_ACCESS_TOKEN"],
        environment=os.environ["FLASK_ENV"],
        root=os.path.dirname(os.path.realpath(__file__)),
        allow_logging_basic_config=False,
    )
    # send exceptions from `app` to rollbar, using flask's signal system
    got_request_exception.connect(rollbar.contrib.flask.report_exception, current_app)
