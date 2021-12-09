import pytest

from prephouse.app_factory import create_test_app
from prephouse.model import db


@pytest.fixture
def client():
    app = create_test_app(db)
    with app.test_client() as client:
        yield client
