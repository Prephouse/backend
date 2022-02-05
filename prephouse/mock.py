import logging
import uuid

from app_factory import create_app
from flask_sqlalchemy import SQLAlchemy
from psycopg2.extras import NumericRange
from sqlalchemy.exc import SQLAlchemyError


def add_commit_rows(_db: SQLAlchemy, *rows):
    """
    Add and commit table rows into the current database session.

    :param _db: a PSQL database instance wrapped in SQLAlchemy
    :param rows: the table rows to be added and committed
    """
    for row in rows:
        _db.session.add(row)
    _db.session.commit()


def insert_mock_values():
    """Create some mock data in the database."""
    from models import db

    create_app(db)

    from models import Engine, Feedback, Question, Upload, UploadQuestion, User

    user1 = User(
        id=uuid.uuid4(),
        first_name="Jadon",
        last_name="Fan",
        email="j53fan@uwaterloo.ca",
        is_admin=True,
    )
    user2 = User(
        id=uuid.uuid4(),
        first_name="Chandler",
        last_name="Lei",
        email="q4lei@uwaterloo.ca",
        is_admin=True,
    )
    add_commit_rows(db, user1, user2)

    questions1 = Question(
        category=Question.QuestionCategory.GENERAL, question="Tell me about yourself"
    )
    add_commit_rows(db, questions1)

    engine1 = Engine(version="0.1.0")
    add_commit_rows(db, engine1)

    upload1 = Upload(
        category=Upload.UploadCategory.INTERVIEW, user_id=user1.id, engine_id=engine1.id, score=1.23
    )
    upload2 = Upload(
        category=Upload.UploadCategory.PRESENTATION, user_id=user1.id, engine_id=engine1.id
    )
    upload3 = Upload(
        category=Upload.UploadCategory.INTERVIEW, user_id=user1.id, engine_id=engine1.id
    )
    add_commit_rows(db, upload1, upload2, upload3)

    uq1 = UploadQuestion(
        upload_id=upload1.id,
        question_id=questions1.id,
    )
    add_commit_rows(db, uq1)

    feedback1 = Feedback(
        uq_id=uq1.id,
        category=Feedback.FeedbackCategory.PAUSE,
        subcategory="test",
        comment="testing...",
        result=2.5,
        confidence=None,
        time_range=NumericRange(1, 10),
        user_report="is this working?",
    )
    add_commit_rows(db, feedback1)


if __name__ == "__main__":
    try:
        insert_mock_values()
    except SQLAlchemyError as e:
        logging.error(e)
