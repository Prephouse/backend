import os

import grpc
from flask import Blueprint
from webargs.flaskparser import use_kwargs

from prephouse.decorators.authentication import private_route
from prephouse.schemas.analysis_schema import analysis_request_schema

analyze_api = Blueprint("analyze_api", __name__, url_prefix="/analyze")


def analyze_callback(feedback_future: grpc.Future, channel: grpc.Channel):
    # TODO save feedback into DB
    feedback_future.result()
    channel.close()
    pass


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
        feedback_future.add_done_callback(lambda future: analyze_callback(future, channel))
    except grpc.RpcError:
        # TODO return error
        return {}

    return {}
