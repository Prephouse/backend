import enum
import os
import uuid

from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from psycopg2.extras import NumericRange
from sqlalchemy.dialects.postgresql import UUID, INT4RANGE
from sqlalchemy.sql import func as sql_func

import constants
from utils import get_integral_numeric_range_bounds

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firebase_token = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    uploads = db.relationship('Upload', backref='user', lazy=True)


class Upload(db.Model):
    class Category(enum.Enum):
        INTERVIEW = 0
        PRESENTATION = 1

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = db.Column(db.Enum(Category), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, server_default=sql_func.now())
    date_modified = db.Column(db.DateTime, server_onupdate=sql_func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedbacks = db.relationship('Feedback', backref='upload', lazy=True)


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
    upload_id = db.Column(UUID(as_uuid=True), db.ForeignKey('upload.id'), nullable=False)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# TODO integrate OAuth check
@app.route("/feedback")
def get_feedback():
    upload_ids = request.args.getlist('upload_ids')
    time_start = request.args.get('time_start', type=int, default=0)
    time_end = request.args.get('time_end', type=int, default=constants.PSQL_INT_MAX)
    feedback_type = request.args.get('feedback_type', type=int)

    query = Feedback.query
    if upload_ids:
        query = query.filter(Feedback.upload_id.in_(upload_ids))
    if feedback_type is not None:
        try:
            feedback_type = Feedback.Type(feedback_type)
        except ValueError:
            abort(400)
        query = query.filter_by(type=feedback_type)
    query = query.filter(Feedback.time_range.contained_by(NumericRange(time_start, time_end)))

    response = []
    for feedback in (query.all() or []):
        time_start, time_end = get_integral_numeric_range_bounds(feedback.time_range)
        response.append({
            'id': feedback.id,
            'upload_id': feedback.upload_id,
            'type': feedback.type.value,
            'text': feedback.text,
            'score': float(feedback.score),
            'time_start': time_start,
            'time_end': time_end,
        })

    return jsonify(response)


if __name__ == '__main__':
    app.run()
