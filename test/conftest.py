from typing import Final

import pytest

from prephouse.app_factory import create_test_app
from prephouse.models import db

PSQL_URI: Final[str] = "postgresql://postgres:postgres@database:5432"
DATABASE_NAME: Final[str] = "prephouse_test"


@pytest.fixture
def client():
    engine = db.create_engine(
        PSQL_URI,
        {
            "isolation_level": "AUTOCOMMIT",
        },
    )
    # TODO replace the following unsafe drop database query
    engine.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME}")
    engine.execute(f"CREATE DATABASE {DATABASE_NAME}")

    app = create_test_app(db, f"{PSQL_URI}/{DATABASE_NAME}")

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            db.session.commit()
            yield client
            db.session.close()
            db.drop_all()
