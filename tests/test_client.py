import pytest

from create_app import create_test_app
from model import db


@pytest.fixture
def client():
    app = create_test_app(db)
    with app.test_client() as client:
        yield client
