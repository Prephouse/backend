import os

import grpc
from flask import Blueprint
from psycopg2.extras import NumericRange
from webargs.flaskparser import use_kwargs

from prephouse.decorators.authentication import private_route
from prephouse.models import Feedback, db
from prephouse.schemas.analysis_schema import analysis_request_schema

analyze_api = Blueprint("analyze_api", __name__, url_prefix="/analyze")


def analyze_callback(feedback_future: grpc.Future, channel: grpc.Channel, upload_link: str):
    try:
        for feedback in feedback_future.result().feedback:
            feedback_row = Feedback(
                category=feedback.category,
                subcategory=feedback.subcategory,
                comment=feedback.comment,
                result=feedback.result,
                confidence=feedback.confidence,
                time_range=NumericRange(int(feedback.time_start), int(feedback.time_end)),
                uq_id=int(upload_link),  # Need to change this once we know url format
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
@private_route
def analyze_upload(upload_link):
    from prephouse_pb2 import Video
    from prephouse_pb2_grpc import PrephouseEngineStub

    credentials = grpc.ssl_channel_credentials()

    try:
        channel = grpc.secure_channel(
            f"{os.environ['ENGINE_GRPC_IP']}:{os.environ['ENGINE_GRPC_PORT']}", credentials
        )
        stub = PrephouseEngineStub(channel)
        feedback_future = stub.GetFeedback.future(Video(link=upload_link))
        feedback_future.add_done_callback(
            lambda future: analyze_callback(future, channel, upload_link)
        )
    except grpc.RpcError:
        # TODO return error
        return {}

    return {}
