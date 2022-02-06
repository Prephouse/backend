import enum
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import INT4RANGE, JSON, UUID
from sqlalchemy.sql import func as sql_func

db = SQLAlchemy()


class User(db.Model):  # type: ignore
    id = db.Column(UUID(as_uuid=True), primary_key=True, autoincrement=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    uploads = db.relationship("Upload", backref="user", lazy=True)


class Engine(db.Model):  # type: ignore
    __table_args__ = (
        db.CheckConstraint(r"version ~ '^\d+.\d+.\d+(-alpha\d{1,2}|-beta\d{1,2}|-RC)?$'"),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version = db.Column(db.String, nullable=False)
    configuration = db.Column(JSON, nullable=False, default={})
    uploads = db.relationship("Upload", backref="engine", lazy=True, uselist=False)


class Upload(db.Model):  # type: ignore
    @enum.unique
    class UploadCategory(enum.IntEnum):
        INTERVIEW = 0
        PRESENTATION = 1

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = db.Column(db.Enum(UploadCategory), nullable=False, index=True)
    score = db.Column(db.Numeric(10, 2), nullable=True)
    date_uploaded = db.Column(db.DateTime, nullable=False, server_default=sql_func.now())
    date_modified = db.Column(db.DateTime, server_onupdate=sql_func.now())
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False)
    engine_id = db.Column(UUID(as_uuid=True), db.ForeignKey("engine.id"))
    filler_words = db.relationship(
        "FillerWord", backref="upload", lazy=True, cascade="all, delete-orphan"
    )
    questions = db.relationship("Question", secondary="upload_question", back_populates="uploads")


class Question(db.Model):  # type: ignore
    @enum.unique
    class QuestionCategory(enum.IntEnum):
        GENERAL = 0
        SOFTWARE = 1
        PRODUCT = 2
        DATA = 3
        BUSINESS = 4
        # TODO complete

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Enum(QuestionCategory), nullable=False)
    question = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    sample_answer = db.Column(db.Text)
    frequency = db.Column(db.Integer)
    uploads = db.relationship("Upload", secondary="upload_question", back_populates="questions")


class UploadQuestion(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(UUID(as_uuid=True), db.ForeignKey("upload.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    feedbacks = db.relationship(
        "Feedback", backref="upload_question", lazy=True, cascade="all, delete-orphan"
    )


class Feedback(db.Model):  # type: ignore
    @enum.unique
    class FeedbackCategory(enum.IntEnum):
        PAUSE = 0
        VOLUME = 1
        LIGHT = 2
        GAZE = 3
        EMOTION = 4
        PITCH = 5

    __table_args__ = (db.CheckConstraint(r"confidence BETWEEN 0 AND 100"),)

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uq_id = db.Column(db.Integer, db.ForeignKey("upload_question.id"), nullable=False)
    category = db.Column(db.Enum(FeedbackCategory), nullable=False)
    subcategory = db.Column(db.String)
    comment = db.Column(db.Text)
    result = db.Column(db.Numeric(10, 2), nullable=False)
    confidence = db.Column(db.Integer)
    time_range = db.Column(INT4RANGE())
    user_report = db.Column(db.Text)


class FillerWord(db.Model):  # type: ignore
    upload_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("upload.id"), primary_key=True, autoincrement=False
    )
    word = db.Column(db.String, primary_key=True, autoincrement=False)
    count = db.Column(db.Integer, nullable=False)
