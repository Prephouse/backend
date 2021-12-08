import os

import grpc
from flask import Blueprint, request

analyze_api = Blueprint("analyze_api", __name__, url_prefix="/analyze")


def analyze_callback(feedback_future: grpc.Future, channel: grpc.Channel):
    # TODO save feedback into DB
    feedback_future.result()
    channel.close()
    pass


@analyze_api.route("/")
def analyze_upload():
    from prephouse.prephouse_pb2 import Video
    from prephouse.prephouse_pb2_grpc import PrephouseEngineStub

    upload_link = request.args.get("upload_link", type=str)

<<<<<<< HEAD
    try:
        channel = grpc.insecure_channel(
            f"{os.environ['ENGINE_GRPC_IP']}:{os.environ['ENGINE_GRPC_PORT']}"
=======
    with grpc.insecure_channel(
        f"{os.environ['ENGINE_GRPC_IP']}:{os.environ['ENGINE_GRPC_PORT']}"
    ) as channel:
        stub = PrephouseEngineStub(channel)
        feedback = stub.GetFeedback(Video(link=upload_link))

        # TODO Save Feedback into DB

        return jsonify(
            [
                {
                    "category": f.category,
                    "comment": f.comment,
                    "score": f.score,
                    "confidence": f.confidence,
                    "time_start": f.timeStart,
                    "time_end": f.timeEnd,
                }
                for f in feedback
            ]
>>>>>>> c3b9c19 (update tables)
        )
        stub = PrephouseEngineStub(channel)
        feedback_future = stub.GetFeedback.future(Video(link=upload_link))
        feedback_future.add_done_callback(lambda future: analyze_callback(future, channel))
    except grpc.RpcError:
        # TODO return error
        return {}

    return {}
