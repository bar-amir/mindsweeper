import grpc
from .protos.code import server_pb2
from .protos.code import server_pb2_grpc
import json
from . import drivers as d
from concurrent import futures
from google.protobuf.json_format import MessageToJson


def publish(message):
    pass

def run_server(host='127.0.0.1', \
               port=8000, \
               publish=None, \
               message_queue_url=None):
    '''listen on host:port and pass received messages to publish'''    
    # Connect to message queue
    global mq
    mq = d.MessageQueue(message_queue_url)

    # Start listening on host:port
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=[
                                            ('grpc.max_send_message_length', 1024 ** 3),
                                            ('grpc.max_receive_message_length', 1024 ** 3)
                                            ])
    server_pb2_grpc.add_MessengerServicer_to_server(Messenger(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

class Messenger(server_pb2_grpc.MessengerServicer):
    def SendUser(self, request, context):
        msg = MessageToJson(request)
        return server_pb2.SendResponse(status_code=1)

    def SendPose(self, request, context):
        msg = MessageToJson(request)
        return server_pb2.SendResponse(status_code=1)

    def SendColorImage(self, request, context):
        bin_path = '' + f'color_images/{request.user_id}/bin/{request.datetime}'
        msg = json.dumps({
            'user_id': request.user_id,
            'datetime': request.datetime,
            'bin_path': bin_path
        })
        print(msg)
        return server_pb2.SendResponse(status_code=1)

    def SendDepthImage(self, request, context):
        newfile = '' + f'depth_images/{request.user_id}/bin/{request.datetime}'
        return server_pb2.SendResponse(status_code=1)

    def SendFeelings(self, request, context):
        msg = MessageToJson(request)
        return server_pb2.SendResponse(status_code=1)

if __name__ == '__main__':
    run_server()