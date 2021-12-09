import enum
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import INT4RANGE, UUID
from sqlalchemy.sql import func as sql_func

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firebase_token = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    uploads = db.relationship("Upload", backref="user", lazy=True)


class Upload(db.Model):
    class Category(enum.Enum):
        INTERVIEW = 0
        PRESENTATION = 1

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = db.Column(db.Enum(Category), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, server_default=sql_func.now())
    date_modified = db.Column(db.DateTime, server_onupdate=sql_func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    feedbacks = db.relationship("Feedback", backref="upload", lazy=True)


class Feedback(db.Model):
    class Type(enum.Enum):
        PAUSE = 0
        SENTIMENT = 1
        # TODO complete

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = db.Column(db.Enum(Type), nullable=False)
    text = db.Column(db.Text)
    score = db.Column(db.Numeric(10, 2), nullable=False)
    time_range = db.Column(INT4RANGE(), nullable=False)
    user_report = db.Column(db.Text)
    upload_id = db.Column(UUID(as_uuid=True), db.ForeignKey("upload.id"), nullable=False)
