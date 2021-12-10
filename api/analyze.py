import os

import grpc
from flask import Blueprint, jsonify, request

from app import app
from prephouse_pb2 import Video
from prephouse_pb2_grpc import PrephouseEngineStub

analyze_api = Blueprint("analyze_api", __name__)


def analyze_callback(feedback_future, channel):
    # TODO: Save Feedback into DB
    feedback = feedback_future.result()
    print(feedback)
    channel.close()
    pass


@app.route("/analyze")
def analyze_upload():
    upload_link = request.args.get("upload_link", type=str)

    try:
        channel = grpc.insecure_channel(
            f"{os.environ['ENGINE_GRPC_IP']}:{os.environ['ENGINE_GRPC_PORT']}"
        )
        stub = PrephouseEngineStub(channel)
        feedback_future = stub.GetFeedback.future(Video(link=upload_link))
        feedback_future.add_done_callback(lambda future: analyze_callback(future, channel))
    except:
        # TODO: Return Error
        pass

    return {}
