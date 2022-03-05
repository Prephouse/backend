import os
import uuid

import grpc
from flask import Blueprint
from psycopg2.extras import NumericRange
from webargs.flaskparser import use_kwargs

from prephouse.models import Feedback, db
from prephouse.schemas.analysis_schema import analysis_request_schema

analyze_api = Blueprint("analyze_api", __name__, url_prefix="/analyze")


def analyze_callback(feedback_future: grpc.Future, channel: grpc.Channel, uq_id: uuid.UUID):
    try:
        for feedback in feedback_future.result().feedback:
            feedback_row = Feedback(
                category=feedback.category,
                subcategory=feedback.subcategory,
                comment=feedback.comment,
                result=feedback.result,
                confidence=feedback.confidence,
                time_range=NumericRange(int(feedback.time_start), int(feedback.time_end)),
                uq_id=uq_id,
            )
            db.session.add(feedback_row)
    except Exception:
        db.session.rollback()
        raise
    else:
        db.session.commit()

    channel.close()
    return


@analyze_api.post("/")
@use_kwargs(analysis_request_schema, location="query")
def analyze_upload(upload_question_id, audio_link, transcript_link, video_link):
    from prephouse_pb2 import MediaList
    from prephouse_pb2_grpc import PrephouseEngineStub

    credentials = grpc.ssl_channel_credentials()

    try:
        channel = grpc.secure_channel(
            f"{os.environ['ENGINE_GRPC_IP']}:{os.environ['ENGINE_GRPC_PORT']}", credentials
        )
        stub = PrephouseEngineStub(channel)
        feedback_future = stub.GetFeedback.future(
            MediaList(audio_link=audio_link, video_link=video_link, transcript_link=transcript_link)
        )
        feedback_future.add_done_callback(
            lambda future: analyze_callback(future, channel, upload_question_id)
        )
    except grpc.RpcError:
        # TODO return error
        return {}

    return {}
