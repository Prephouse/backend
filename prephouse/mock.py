import logging
import random
from typing import Any

from app_factory import create_app
from faker import Faker
from flask_sqlalchemy import SQLAlchemy
from psycopg2.extras import NumericRange
from sqlalchemy.dialects.postgresql import insert as psql_insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.inspection import inspect


def upsert(_db: SQLAlchemy, table: Any, **values):
    """
    Upsert values into some DB table.

    :param _db: a PSQL database instance wrapped in SQLAlchemy
    :param table: model class for the corresponding DB table
    :param values: the values to upsert
    """
    pks = [pk.name for pk in inspect(table).primary_key]
    stmt = (
        psql_insert(table)
        .values(**values)
        .on_conflict_do_update(
            index_elements=pks, set_={k: v for k, v in values.items() if k not in pks}
        )
    )
    _db.session.execute(stmt)
    _db.session.commit()

    results = table.query.all()
    random.shuffle(results)

    return results[0]


def insert_mock_values():
    """Create some mock data in the database."""
    from models import db

    create_app(db, False)

    from models import Engine, Feedback, Question, Upload, UploadQuestion, User

    fake = Faker()
    try:
        users = [
            upsert(
                db,
                User,
                id=fake.uuid4(),
                name=fake.name(),
                email=fake.email(),
                is_admin=fake.boolean(),
            )
            for _ in range(10)
        ]

        questions = [
            upsert(
                db,
                Question,
                category=random.choice(list(Question.QuestionCategory)),
                question=fake.text(max_nb_chars=20),
                description=fake.text(max_nb_chars=50),
                frequency=random.randrange(100),
            )
            for _ in range(10)
        ]

        engine = Engine.query.filter_by(version="0.1.0").first()
        if not engine:
            engine = upsert(db, Engine, version="0.1.0")
        engines = [engine]

        uploads = [
            upsert(
                db,
                Upload,
                category=random.choice(list(Upload.UploadCategory)),
                user_id=random.choice(users).id,
                engine_id=random.choice(engines).id,
                score=random.uniform(0, 100),
            )
            for _ in range(10)
        ]

        upload_questions = [
            upsert(
                db,
                UploadQuestion,
                upload_id=random.choice(uploads).id,
                question_id=random.choice(questions).id,
                cloudfront_url="http://d2949o5mkkp72v.cloudfront.net",
                manifest_file="manifest_file",
            )
            for _ in range(5)
        ]

        for _ in range(5):
            upsert(
                db,
                Feedback,
                uq_id=random.choice(upload_questions).id,
                category=random.choice(list(Feedback.FeedbackCategory)),
                subcategory="test",
                result=random.uniform(0, 100),
                confidence=random.uniform(0, 1),
                time_range=NumericRange(1, 10),
            )
        for feature in Feedback.FeedbackCategory:
            upsert(
                db,
                Feedback,
                uq_id=random.choice(upload_questions).id,
                category=feature,
                subcategory="score",
                comment=fake.text(max_nb_chars=20),
                result=random.uniform(0, 100),
                confidence=None,
                time_range=NumericRange(1, 10),
                user_report=fake.text(max_nb_chars=50),
            )
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(e)
    finally:
        db.session.close()


if __name__ == "__main__":
    insert_mock_values()
