import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(_db: SQLAlchemy) -> Flask:
    """
    Create a Flask app for staging and production environments with the corresponding database.

    :arg _db: a PSQL database instance wrapped in SQLAlchemy
    :return: the Flask app instance with the proper configurations for staging
              and prod environments
    """
    _app = Flask(__name__)
    _app.config |= {
        "SQLALCHEMY_DATABASE_URI": os.environ["SQLALCHEMY_DATABASE_URI"],
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    _db.init_app(_app)
    _app.app_context().push()
    return _app


def create_test_app(_db: SQLAlchemy, _db_uri: str) -> Flask:
    """
    Create a Flask app for test environment with a modifiable database.

    :arg _db: a PSQL database instance wrapped in SQLAlchemy
    :arg _db_uri: the PSQL URI **without** a specified database
    :return: the Flask app instance with the proper configurations for the test environment
    """
    _app = Flask(__name__)
    _app.config |= {
        "SQLALCHEMY_DATABASE_URI": _db_uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "TESTING": True,
    }
    _db.init_app(_app)
    _app.app_context().push()
    return _app
