import argparse
import os
import uuid
from typing import Any

from app_factory import create_app
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from psycopg2.extras import NumericRange


def add_commit_rows(_db: SQLAlchemy, *rows: tuple[Any, ...]):
    """
    Add and commit table rows into the current database session.

    :param _db: a PSQL database instance wrapped in SQLAlchemy
    :param rows: the table rows to be added and committed
    """
    for row in rows:
        _db.session.add(row)
    _db.session.commit()


def create_schema(requested_mock_data: bool = False):
    """
    Create the prephouse database and, if requested, some mock data for the database.

    :param requested_mock_data: `True` if mock data should be included after the database
           is created; `False` otherwise
    """
    if not (load_dotenv("../.env.development") and os.environ.get("FLASK_ENV") == "development"):
        return

    from model import db

    create_app(db)
    db.create_all()

    if requested_mock_data:

        from model import Engine, Feedback, Upload, User

        user1 = User(
            first_name="Jadon",
            last_name="Fan",
            email="j53fan@uwaterloo.ca",
            firebase_token=uuid.uuid4(),
            is_admin=True,
        )
        user2 = User(
            first_name="Chandler",
            last_name="Lei",
            email="q4lei@uwaterloo.ca",
            firebase_token=uuid.uuid4(),
            is_admin=True,
        )
        add_commit_rows(db, user1, user2)

        engine1 = Engine(version="0.1.0")
        add_commit_rows(db, engine1)

        upload1 = Upload(category=Upload.Category.INTERVIEW, user_id=user1.id, engine_id=engine1.id)
        upload2 = Upload(
            category=Upload.Category.PRESENTATION, user_id=user1.id, engine_id=engine1.id
        )
        upload3 = Upload(category=Upload.Category.INTERVIEW, user_id=user1.id, engine_id=engine1.id)
        add_commit_rows(db, upload1, upload2, upload3)

        feedback1 = Feedback(
            category=Feedback.Feature.PAUSE,
            comment="testing...",
            score=2.5,
            confidence=None,
            time_range=NumericRange(1, 10),
            user_report="is this working?",
            upload_id=upload1.id,
        )
        add_commit_rows(db, feedback1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mock", dest="requested_mock_data", action="store_true")
    args = parser.parse_args()

    create_schema(args.requested_mock_data)
