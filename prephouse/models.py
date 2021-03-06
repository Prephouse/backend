import enum
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import INT4RANGE, JSON, UUID
from sqlalchemy.sql import func as sql_func

db = SQLAlchemy()


class User(db.Model):  # type: ignore
    """
    A single Prephouse user.

    :cvar id: firebase uid
    :cvar name: full username
    :cvar email: email address
    :cvar is_admin: `True` if the user has admin privileges, `False` otherwise
    :cvar uploads: past interview/presentation sessions for this user
    """

    id = db.Column(db.String, primary_key=True, autoincrement=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    uploads = db.relationship("Upload", backref="user", lazy=True)


class Engine(db.Model):  # type: ignore
    """
    A unique analyzer engine instance.

    :cvar id: engine UUID, should always be autogenerated
    :cvar version: version of engine used
    :cvar configuration: engine feature configurations, such as the silent pause threshold
    :cvar uploads: past interview/presentation sessions that were analyzed with this engine instance
    """

    __table_args__ = (
        db.CheckConstraint(r"version ~ '^\d+.\d+.\d+(-alpha\d{1,2}|-beta\d{1,2}|-RC)?$'"),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version = db.Column(db.String, nullable=False, unique=True, index=True)
    configuration = db.Column(JSON, nullable=False, default={})
    uploads = db.relationship("Upload", backref="engine", lazy=True, uselist=False)


class Upload(db.Model):  # type: ignore
    """
    A single entire interview or presentation session.

    One upload may contain multiple questions.

    :cvar id: interview/presentation session id, should be autogenerated
    :cvar category: interview or presentation
    :cvar score: overall score across all questions for this interview/presentation session
    :cvar date_uploaded: date when the interview/presentation session was recorded or
                         uploaded by user
    :cvar date_modified: date when the interview/presentation session was last updated by server
    :cvar user_id: id of the user for this interview/presentation session
    :cvar engine_id: id of the analyzer engine instance used for this interview/presentation session
    :cvar questions: questions asked for this interview/presentation session
    """

    @enum.unique
    class UploadCategory(enum.IntEnum):
        INTERVIEW = 0
        PRESENTATION = 1

        def get_category_name(self) -> str | None:
            match self:
                case self.INTERVIEW:
                    return "Interview"
                case self.PRESENTATION:
                    return "Presentation"
            return None

    @enum.unique
    class UploadMedium(enum.IntEnum):
        VIDEO_AUDIO = 0
        AUDIO_ONLY = 1

    @enum.unique
    class UploadOrigin(enum.IntEnum):
        RECORD = 0
        UPLOAD = 1

    __table_args__ = (db.CheckConstraint(r"score BETWEEN 0 and 100"),)

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = db.Column(db.Enum(UploadCategory), nullable=False, index=True)
    score = db.Column(db.Numeric(10, 2))
    date_uploaded = db.Column(db.DateTime, nullable=False, server_default=sql_func.now())
    date_modified = db.Column(db.DateTime, server_onupdate=sql_func.now())
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    engine_id = db.Column(UUID(as_uuid=True), db.ForeignKey("engine.id"))
    questions = db.relationship("Question", secondary="upload_question", back_populates="uploads")


class Question(db.Model):  # type: ignore
    """
    A unique question that could be selected for an interview session.

    A single question from this table could be used in multiple uploads in the
    `UploadQuestion` table.

    :cvar id: question id, should be autogenerated
    :cvar category: question category
    :cvar question: question
    :cvar description: contextual description of this question
    :cvar sample_answer: an exemplar answer
    :cvar frequency: number of times that this question has been asked across all uploads and users
    :cvar uploads: the interview/presentation sessions where this question was asked
    """

    @enum.unique
    class QuestionCategory(enum.IntEnum):
        GENERAL = 0
        SOFTWARE = 1
        PRODUCT = 2
        DATA = 3
        BUSINESS = 4

        def get_category_name(self) -> str | None:
            match self:
                case self.GENERAL:
                    return "General"
                case self.SOFTWARE:
                    return "Software"
                case self.PRODUCT:
                    return "Product"
                case self.DATA:
                    return "Data"
                case self.BUSINESS:
                    return "Business"
            return None

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Enum(QuestionCategory), nullable=False)
    question = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    sample_answer = db.Column(db.Text)
    frequency = db.Column(db.Integer)
    uploads = db.relationship("Upload", secondary="upload_question", back_populates="questions")


class UploadQuestion(db.Model):  # type: ignore
    """
    A single question tied to a particular upload.

    Where there exists multiple rows with the same upload ID but different question IDs in this
    table, the questions corresponding to those question IDs were asked for the upload (interview
    session) with that particular upload ID.

    :cvar id: upload question id, should be autogenerated
    :cvar upload_id: ID of the upload (interview session) where the question with the specified
                     question ID was asked
    :cvar question_id: ID of the question that was asked in the upload with the specified upload ID
    :cvar textual_summary: summary of users response
    :cvar cloudfront_url: cloudfront URL where the user response to this upload question
                          can be found
    :cvar manifest_file: path to the cloudfront manifest file
    :cvar feedbacks: the feedbacks generated by the analyzer engine for this upload question
    """

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    upload_id = db.Column(UUID(as_uuid=True), db.ForeignKey("upload.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    textual_summary = db.Column(db.Text)
    cloudfront_url = db.Column(db.Text)
    manifest_file = db.Column(db.Text)
    feedbacks = db.relationship(
        "Feedback", backref="upload_question", lazy=True, cascade="all, delete-orphan"
    )


class Feedback(db.Model):  # type: ignore
    """
    A single piece of feedback generated by the analyzer engine.

    Note: Recall that the feedback is sent through the Prephouse gRPC service, so it
    may be helpful to look through the corresponding protobuf in the analyzer-engine
    repo when working with this table.

    :cvar id: feedback ID, should be autogenerated
    :cvar uq_id: ID of the upload question that is being addressed by this feedback
    :cvar category: corresponding analyzer engine feature
    :cvar subcategory: type of feedback for the specified engine feature
    :cvar comment: textual feedback
    :cvar result: numerical feedback
    :cvar confidence: confidence interval for the accuracy of this feedback
    :cvar time_range: the range of timestamps in the interview/presentation session
                      where this feedback is applicable
    :cvar user_report: concerns and complaints reported by the user about this feedback
    """

    @enum.unique
    class FeedbackCategory(enum.IntEnum):
        PAUSE = 1
        VOLUME = 2
        LIGHT = 3
        GAZE = 4
        EMOTION = 5
        PITCH = 6
        FILLER_WORD = 7
        TEXTUAL_SUMMARY = 8

        @classmethod
        def get_video_only_features(cls) -> set["Feedback.FeedbackCategory"]:
            return {cls.LIGHT, cls.GAZE, cls.EMOTION}

        def get_feature_name(self) -> str | None:
            match self:
                case self.PAUSE:
                    return "Silent Pauses"
                case self.VOLUME:
                    return "Volume"
                case self.LIGHT:
                    return "Background Light"
                case self.GAZE:
                    return "Gaze Direction"
                case self.EMOTION:
                    return "Emotion"
                case self.PITCH:
                    return "Pitch"
                case self.FILLER_WORD:
                    return "Filler Words"
                case self.TEXTUAL_SUMMARY:
                    return "Textual Summary"
            return None

        def get_api_safe_feature_name(self) -> str | None:
            name = self.get_feature_name()
            return name.lower().replace(" ", "_") if name else name

    __table_args__ = (db.CheckConstraint(r"confidence BETWEEN 0 AND 1"),)

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uq_id = db.Column(UUID(as_uuid=True), db.ForeignKey("upload_question.id"), nullable=False)
    category = db.Column(db.Enum(FeedbackCategory), nullable=False)
    subcategory = db.Column(db.String)
    comment = db.Column(db.Text)
    result = db.Column(db.Numeric(10, 2), nullable=False)
    confidence = db.Column(db.Numeric(10, 9))
    time_range = db.Column(INT4RANGE())
    user_report = db.Column(db.Text)
