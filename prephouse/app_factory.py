import os

from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import DENY, Talisman


def create_app(_db: SQLAlchemy) -> Flask:
    """
    Create a Flask app for staging and production environments with the corresponding database.

    :arg _db: a PSQL database instance wrapped in SQLAlchemy
    :return: the Flask app instance with the proper configurations for staging
              and prod environments
    """
    # Initialize Flask application
    _app = Flask(__name__)
    _app.config |= {
        "SECRET_KEY": os.environ["FLASK_SECRET_KEY"],
        "SQLALCHEMY_DATABASE_URI": os.environ["SQLALCHEMY_DATABASE_URI"],
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "CSRF_COOKIE_HTTPONLY": True,
        "CSRF_COOKIE_SECURE": True,
    }

    # TODO: Limit by User instead of IP when auth is done
    limiter = Limiter(
        _app, key_func=get_remote_address, default_limits=["5 per second", "1000 per day"]
    )

    # Configure web security measures such as CSP, CORS, HSTS and CSRF
    Talisman(
        _app,
        frame_options=DENY,
        content_security_policy={
            "default-src": "'none'",
            "frame-ancestors": "'none'",
            "require-trusted-types-for": "'script'",
        },
    )
    CORS(_app, support_credentials=True, origins=["*" if _app.debug else "https://prephouse.io"])
    csrf = SeaSurf()
    csrf.init_app(_app)

    # Initialize PostgreSQL database
    _db.init_app(_app)

    # Bind app context
    _app.app_context().push()

    return _app


def create_test_app(_db: SQLAlchemy, _db_uri: str) -> Flask:
    """
    Create a Flask app for test environment with a modifiable database.

    :arg _db: a PSQL database instance wrapped in SQLAlchemy
    :arg _db_uri: the PSQL URI **without** a specified database
    :return: the Flask app instance with the proper configurations for the test environment
    """
    from secrets import token_hex

    # Initialize Flask application
    _app = Flask(__name__)
    _app.config |= {
        "SECRET_KEY": token_hex(16),
        "SQLALCHEMY_DATABASE_URI": _db_uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "TESTING": True,
    }

    # Initialize PostgreSQL database
    _db.init_app(_app)

    # Bind app context
    _app.app_context().push()

    return _app
