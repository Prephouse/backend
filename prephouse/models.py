import enum
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import INT4RANGE, JSON, UUID
from sqlalchemy.sql import func as sql_func

db = SQLAlchemy()


class User(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firebase_token = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    uploads = db.relationship("Upload", backref="user", lazy=True)


class Engine(db.Model):  # type: ignore
    __table_args__ = (
        db.CheckConstraint(r"version ~ '^\d+.\d+.\d+(-alpha\d{1,2}|-beta\d{1,2}|-RC)?$'"),
    )

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String, nullable=False)
    configuration = db.Column(JSON, nullable=False, default={})
    uploads = db.relationship("Upload", backref="engine", lazy=True, uselist=False)


class Upload(db.Model):  # type: ignore
    @enum.unique
    class Category(enum.IntEnum):
        INTERVIEW = 0
        PRESENTATION = 1

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = db.Column(db.Enum(Category), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, server_default=sql_func.now())
    date_modified = db.Column(db.DateTime, server_onupdate=sql_func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    engine_id = db.Column(db.Integer, db.ForeignKey("engine.id"))
    feedbacks = db.relationship("Feedback", backref="upload", lazy=True)
    suggestions = db.relationship("Suggestion", backref="upload", lazy=True)
    filler_words = db.relationship("FillerWord", backref="upload", lazy=True)
    questions = db.relationship("Question", backref="upload", lazy=True)


class Feedback(db.Model):  # type: ignore
    # Flask-SQLAlchemy is not able to resolve inner classes of the same name
    # even if their outer classes have different names, hence this enum class
    # name does not match the corresponding table column name
    # TODO Jadon — investigate
    @enum.unique
    class Feature(enum.IntEnum):
        PAUSE = 0
        VOLUME = 1
        LIGHT = 2
        GAZE = 3
        EMOTION = 4
        PITCH = 5

    __table_args__ = (db.CheckConstraint(r"confidence BETWEEN 0 AND 100"),)

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = db.Column(db.Enum(Feature), nullable=False)
    subcategory = db.Column(db.String)
    comment = db.Column(db.Text)
    result = db.Column(db.Numeric(10, 2), nullable=False)
    confidence = db.Column(db.Integer)
    time_range = db.Column(INT4RANGE())
    user_report = db.Column(db.Text)
    upload_id = db.Column(UUID(as_uuid=True), db.ForeignKey("upload.id"), nullable=False)


class Question(db.Model):  # type: ignore
    @enum.unique
    class Category(enum.IntEnum):
        GENERAL = 0
        SOFTWARE = 1
        PRODUCT = 2
        DATA = 3
        BUSINESS = 4
        # TODO complete

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = db.Column(db.Enum(Category), nullable=False)
    question = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    sample_answer = db.Column(db.Text)
    frequency = db.Column(db.Integer)


class Suggestion(db.Model):  # type: ignore
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comment = db.Column(db.Text)
    upload_id = db.Column(UUID(as_uuid=True), db.ForeignKey("upload.id"), nullable=False)


class FillerWord(db.Model):  # type: ignore
    upload_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("upload.id"), primary_key=True, autoincrement=False
    )
    word = db.Column(db.String, primary_key=True, autoincrement=False)
    count = db.Column(db.Integer, nullable=False)
