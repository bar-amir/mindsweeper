import grpc
from .protos.code import server_pb2_grpc
from . import reader

def upload_sample(host='127.0.0.1', \
                  port=8000, \
                  path=None):
    '''upload path to host:port'''

    # Connect to host:port
    with grpc.insecure_channel(f'{host}:{port}') as channel:
        stub = server_pb2_grpc.MessengerStub(channel)

        r = reader.Reader(path)
        
        # Send UserMessage to server
        response = stub.SendUser(r.UserMessage)
        print(response)

        # Send other messages to server
        for i in r:
            func = stub.__dict__['Send' + type(i).__name__.replace('Message', '')]
            response = func(i)

        # Close connection

    pass

if __name__ == '__main__':
    upload_sample(path='/home/baram/Documents/mindsweeper/sample.mind.gz')