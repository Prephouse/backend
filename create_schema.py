import argparse
import os
import uuid
from typing import Any

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from psycopg2.extras import NumericRange


def add_commit_rows(db: SQLAlchemy, *rows: tuple[Any, ...]):
    for row in rows:
        db.session.add(row)
    db.session.commit()


def create_schema(requested_mock_data: bool = False):
    if load_dotenv(".env.development") and os.environ.get("FLASK_ENV") == "development":
        from app import create_app, db

        create_app()
        db.create_all()

        if requested_mock_data:

            from app import Feedback, Upload, User

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

            upload1 = Upload(category=Upload.Category.INTERVIEW, user_id=user1.id)
            upload2 = Upload(category=Upload.Category.PRESENTATION, user_id=user1.id)
            upload3 = Upload(category=Upload.Category.INTERVIEW, user_id=user1.id)
            add_commit_rows(db, upload1, upload2, upload3)

            feedback1 = Feedback(
                type=Feedback.Type.SENTIMENT,
                text="testing...",
                score=2.5,
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
