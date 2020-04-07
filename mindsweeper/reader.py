import gzip
import struct
from .protos import default_pb2

class Reader:
"""
TODO make paths portable, documentation, api, cli
"""
    def __init__(self, path, format):
        self.path = path
        self.format = format
        self.g = self.rd()
        self.user = default_pb2.User()
        self.user.ParseFromString(next(self.g))
        self.snapshot = default_pb2.Snapshot()
    def __repr__(self):
        return '<Reader "">'
    
    def __str__(self):
        pass

    def __iter__(self):
        while True:
            self.snapshot.ParseFromString(next(self.g))
            yield self.snapshot

    def rd(self):
        with gzip.open(self.path, 'rb') as f:
            size = 4
            for chunk in iter(lambda: f.read(size), b''):
                if size == 4:
                    # reading message size
                    size = struct.unpack('<I', chunk)[0]
                else:
                    # yielding actual message
                    yield chunk
                    size = 4

if __name__ == '__main__':
    reader = Reader('sample.mind.gz', 'mindsweeper/protos/default.proto')
    print(reader.user)