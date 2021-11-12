import os

import grpc
from flask import jsonify, request, Blueprint

from app import app
from prephouse_pb2 import Video
from prephouse_pb2_grpc import PrephouseEngineStub

analyze_api = Blueprint("analyze_api", __name__)


@app.route("/analyze")
def analyze_upload():
    upload_link = request.args.get("upload_link", type=str)

    with grpc.insecure_channel(
        f"{os.environ['ENGINE_GRPC_IP']}:{os.environ['ENGINE_GRPC_PORT']}"
    ) as channel:
        stub = PrephouseEngineStub(channel)
        feedback = stub.GetFeedback(Video(link=upload_link))

        # TODO: Save Feedback into DB

        return jsonify(
            [
                {
                    "type": f.type,
                    "text": f.text,
                    "score": f.score,
                    "time_start": f.timeStart,
                    "time_end": f.timeEnd,
                }
                for f in feedback
            ]
        )
