import struct
import gzip
import sys
import importlib
from pathlib import Path
import click
from .. import config
import time


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

    def load_proto_code(self):
        root = config.PROJECT_ROOT / 'mindsweeper' / 'protos' / 'code'
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
        snapshots_counter = 0
        with self.open(self.path, 'rb') as f:
            click.echo(click.style('Getting things ready...', fg='yellow'))
            # First yield is a sweepSummary
            sweep_start = None
            sweep_end = None
            msg_len_bytes = f.read(4)
            cursor_snapshots = 4 + struct.unpack('I', msg_len_bytes)[0]
            while len(msg_len_bytes) > 0:
                msg_len = struct.unpack('I', msg_len_bytes)[0]
                if (f.tell() == 4):
                    user = self.pb2.User()
                    user.ParseFromString(f.read(msg_len))
                    msg = {
                        'type': 'user',
                        'status': 'uploaded',
                        'userId': user.user_id,
                        'datetime': int(time.time()),
                        'data': {
                            'username': user.username,
                            'birthday': user.birthday,
                            'gender': user.gender,
                        }
                    }
                    yield msg
                else:
                    snapshot = self.pb2.Snapshot()
                    snapshot.ParseFromString(f.read(msg_len))
                    if not sweep_end or snapshot.datetime > sweep_end:
                        sweep_end = snapshot.datetime
                    if not sweep_start or snapshot.datetime < sweep_start:
                        sweep_start = snapshot.datetime
                    snapshots_counter += 1
                msg_len_bytes = f.read(4)
            msg = {
                'type': 'sweep_summary',
                'status': 'uploaded',
                'userId': user.user_id,
                'datetime': int(time.time()),
                'data': {
                    'sweepStart': sweep_start,
                    'sweepEnd': sweep_end,
                    'numOfSnapshots': snapshots_counter
                }
            }
            yield msg
            f.seek(cursor_snapshots)
        #with self.open(self.path, 'rb') as f:
            with click.progressbar(length=snapshots_counter, label=click.style('Uploading sweep...', fg='yellow')) as bar:
                msg_len_bytes = f.read(4)
                while len(msg_len_bytes) > 0:
                    msg_len = struct.unpack('I', msg_len_bytes)[0]
                    snapshot = self.pb2.Snapshot()
                    snapshot.ParseFromString(f.read(msg_len))
                    msg = {
                        'type': 'pose',
                        'status': 'uploaded',
                        'userId': user.user_id,
                        'datetime': snapshot.datetime,
                        'data': {
                            'translation': {
                                'x': snapshot.pose.translation.x,
                                'y': snapshot.pose.translation.y,
                                'z': snapshot.pose.translation.z
                            },
                            'rotation': {
                                'x': snapshot.pose.rotation.x,
                                'y': snapshot.pose.rotation.y,
                                'z': snapshot.pose.rotation.z,
                                'w': snapshot.pose.rotation.w
                            }
                        }
                    }
                    yield msg
                    msg = {
                        'type': 'color_image',
                        'status': 'uploaded',
                        'userId': user.user_id,
                        'datetime': snapshot.datetime,
                        'data': {
                            'width': snapshot.color_image.width,
                            'height': snapshot.color_image.height,
                            'data': snapshot.color_image.data
                        }
                    }
                    yield msg
                    msg = {
                        'type': 'depth_image',
                        'status': 'uploaded',
                        'tell': f.tell(),
                        'userId': user.user_id,
                        'datetime': snapshot.datetime,
                        'data': {
                            'width': snapshot.depth_image.width,
                            'height': snapshot.depth_image.height,
                            #'data': snapshot.depth_image.data
                        }
                    }
                    yield msg
                    msg = {
                        'type': 'feelings',
                        'status': 'uploaded',
                        'userId': user.user_id,
                        'datetime': snapshot.datetime,
                        'data': {
                            'hunger': snapshot.feelings.hunger,
                            'thirst': snapshot.feelings.thirst,
                            'exhaustion': snapshot.feelings.exhaustion,
                            'happiness': snapshot.feelings.happiness
                        }
                    }
                    yield msg
                    bar.update(1)
                    msg_len_bytes = f.read(4)
        raise StopIteration()
