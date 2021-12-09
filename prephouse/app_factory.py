import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(_db: SQLAlchemy) -> Flask:
    _app = Flask(__name__)
    _app.config |= {
        "SQLALCHEMY_DATABASE_URI": os.environ["SQLALCHEMY_DATABASE_URI"],
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    _db.init_app(_app)
    _app.app_context().push()
    return _app


def create_test_app(_db: SQLAlchemy) -> Flask:
    _app = Flask(__name__)
    _app.config |= {
        "SQLALCHEMY_DATABASE_URI": os.environ["SQLALCHEMY_DATABASE_URI_TEST"],
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "TESTING": True,
    }
    _db.init_app(_app)
    _app.app_context().push()
    return _app
