from .protos.code import server_pb2 as spb2
import struct
import gzip
import os
import sys
import importlib
from pathlib import Path

class Reader:
    def __init__(self, path):
        fmt, *ext = Path(path).suffixes
        self.fmt = fmt[1:]
        self.path = path
        self.is_gzipped = '.gz' in ext
        # Choose reader function
        self.gen = Reader.__dict__[self.fmt + '_reader'](self)
        # Import relevant module
        self.load_proto_code()
        # Get server UserMessage
        self.UserMessage = next(self.gen)

    def load_proto_code(self):
        root = Path(os.path.dirname(os.path.realpath(__file__)) + '/protos/code')
        sys.path.insert(0, str(root))
        pb2_name = f'mindsweeper.protos.code.{self.fmt}_pb2'
        importlib.import_module(pb2_name, package=root.name)
        self.pb2 = sys.modules[pb2_name]
    
    def __iter__(self):
        yield from self.gen

    # Implement your own reader functions below here.
    # Make sure the signature is <file_extension>_reader(self)
    # Handling gzipped files is up to you.

    def mind_reader(self):
        # Determine how to open the file according to its extension
        self.open = gzip.open if self.is_gzipped else open
        with self.open(self.path, 'rb') as f:
            # First yield must be a server UserMessage
            msg_len_bytes = f.read(4)
            while len(msg_len_bytes) > 0:
                msg_len = struct.unpack('I', msg_len_bytes)[0]

                if (f.tell() == 4):
                    user = self.pb2.User()
                    user.ParseFromString(f.read(msg_len))

                    user_msg          = spb2.UserMessage()
                    user_msg.user_id  = user.user_id
                    user_msg.username = user.username
                    user_msg.birthday = user.birthday
                    user_msg.gender   =  user.gender
                    
                    yield user_msg
                else:
                    snapshot = self.pb2.Snapshot()
                    snapshot.ParseFromString(f.read(msg_len))
                    
                    pose_msg               = spb2.PoseMessage()
                    pose_msg.user_id       = self.UserMessage.user_id
                    pose_msg.datetime      = snapshot.datetime
                    pose_msg.translation.x = snapshot.pose.translation.x
                    pose_msg.translation.y = snapshot.pose.translation.y
                    pose_msg.translation.z = snapshot.pose.translation.z
                    pose_msg.rotation.x    = snapshot.pose.rotation.x
                    pose_msg.rotation.y    = snapshot.pose.rotation.y
                    pose_msg.rotation.z    = snapshot.pose.rotation.z
                    pose_msg.rotation.w    = snapshot.pose.rotation.w
                    yield pose_msg

                    color_image_msg          = spb2.ColorImageMessage()
                    color_image_msg.user_id  = self.UserMessage.user_id
                    color_image_msg.datetime = snapshot.datetime
                    color_image_msg.width    = snapshot.color_image.width
                    color_image_msg.height   = snapshot.color_image.height
                    color_image_msg.data     = snapshot.color_image.data
                    yield color_image_msg

                    depth_image_msg          = spb2.DepthImageMessage()
                    depth_image_msg.user_id  = self.UserMessage.user_id
                    depth_image_msg.datetime = snapshot.datetime
                    depth_image_msg.width    = snapshot.depth_image.width
                    depth_image_msg.height   = snapshot.depth_image.height
                    depth_image_msg.data[:]  = snapshot.depth_image.data
                    yield depth_image_msg

                    feelings_msg            = spb2.FeelingsMessage()
                    feelings_msg.user_id    = self.UserMessage.user_id
                    feelings_msg.datetime   = snapshot.datetime
                    feelings_msg.hunger     = snapshot.feelings.hunger
                    feelings_msg.thirst     = snapshot.feelings.thirst
                    feelings_msg.exhaustion = snapshot.feelings.exhaustion
                    feelings_msg.happiness  = snapshot.feelings.happiness
                    yield feelings_msg

                msg_len_bytes = f.read(4)

if __name__ == '__main__':
    r = Reader('/home/baram/Documents/mindsweeper/sample.mind.gz')
    for i in iter(r):
        pass