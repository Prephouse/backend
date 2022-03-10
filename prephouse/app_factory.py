import os

from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import DENY, Talisman


def create_app(_db: SQLAlchemy, with_internal: bool = True) -> Flask:
    """
    Create a Flask app for staging and production environments with the corresponding database.

    :arg _db: a PSQL database instance wrapped in SQLAlchemy
    :arg with_internal: `True` to set internal classes, `False` otherwise
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
    _app.url_map.strict_slashes = False

    # Set internal classes
    if with_internal:
        from prephouse.internal import PrephouseRequest

        _app.request_class = PrephouseRequest

    # Limit API call rates
    Limiter(_app, key_func=get_remote_address, default_limits=["5 per second", "1000 per day"])

    # Configure web security measures such as CSP, XSS protections and HSTS
    Talisman(
        _app,
        frame_options=DENY,
        content_security_policy={
            "default-src": "'none'",
            "frame-ancestors": "'none'",
            "require-trusted-types-for": "'script'",
        },
    )

    # Configure CORS
    if _app.debug:
        origins = ["*"]
    else:
        origins = ["https://prephouse.io", "https://www.prephouse.io", "https://api.prephouse.io"]
    CORS(_app, support_credentials=True, origins=origins)

    # Configure CSRF
    if not _app.debug:
        SeaSurf().init_app(_app)

    # Initialize PostgreSQL database
    _db.init_app(_app)

    # Set up database migrations
    Migrate(compare_type=True).init_app(_app, _db)

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
