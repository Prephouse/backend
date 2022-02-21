# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import prephouse_pb2 as prephouse__pb2


class PrephouseEngineStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetFeedback = channel.unary_unary(
                '/PrephouseEngine/GetFeedback',
                request_serializer=prephouse__pb2.MediaList.SerializeToString,
                response_deserializer=prephouse__pb2.FeedbackList.FromString,
                )
        self.GetMockFeedback = channel.unary_unary(
                '/PrephouseEngine/GetMockFeedback',
                request_serializer=prephouse__pb2.MediaList.SerializeToString,
                response_deserializer=prephouse__pb2.FeedbackList.FromString,
                )
        self.GetMockFeedback = channel.unary_unary(
                '/PrephouseEngine/GetMockFeedback',
                request_serializer=prephouse__pb2.Video.SerializeToString,
                response_deserializer=prephouse__pb2.FeedbackList.FromString,
                )


class PrephouseEngineServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetFeedback(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMockFeedback(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PrephouseEngineServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetFeedback': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFeedback,
                    request_deserializer=prephouse__pb2.MediaList.FromString,
                    response_serializer=prephouse__pb2.FeedbackList.SerializeToString,
            ),
            'GetMockFeedback': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMockFeedback,
                    request_deserializer=prephouse__pb2.MediaList.FromString,
                    response_serializer=prephouse__pb2.FeedbackList.SerializeToString,
            ),
            'GetMockFeedback': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMockFeedback,
                    request_deserializer=prephouse__pb2.Video.FromString,
                    response_serializer=prephouse__pb2.FeedbackList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PrephouseEngine', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PrephouseEngine(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetFeedback(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PrephouseEngine/GetFeedback',
            prephouse__pb2.MediaList.SerializeToString,
            prephouse__pb2.FeedbackList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMockFeedback(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PrephouseEngine/GetMockFeedback',
            prephouse__pb2.MediaList.SerializeToString,
            prephouse__pb2.FeedbackList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMockFeedback(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PrephouseEngine/GetMockFeedback',
            prephouse__pb2.Video.SerializeToString,
            prephouse__pb2.FeedbackList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
