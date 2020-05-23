import click
import gzip
import struct
import time
from . import proto_reader


@proto_reader
def mind(path, proto):
    if path.endswith('.gz'):
        open_func = gzip.open
    else:
        open_func = open
    snapshots_counter = 0
    with open_func(path, 'rb') as f:
        click.echo(click.style('Getting things ready...', fg='yellow'))
        sweep_start = None
        sweep_end = None
        msg_len_bytes = f.read(4)
        cursor_snapshots = 4 + struct.unpack('I', msg_len_bytes)[0]
        while len(msg_len_bytes) > 0:
            msg_len = struct.unpack('I', msg_len_bytes)[0]
            if (f.tell() == 4):
                user = proto.User()
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
                snapshot = proto.Snapshot()
                snapshot.ParseFromString(f.read(msg_len))
                if not sweep_end or snapshot.datetime > sweep_end:
                    sweep_end = snapshot.datetime
                if not sweep_start or snapshot.datetime < sweep_start:
                    sweep_start = snapshot.datetime
                snapshots_counter += 1
            msg_len_bytes = f.read(4)
        msg = {
            'type': 'sweep',
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
        with click.progressbar(length=snapshots_counter,
                               label=click.style(
                                   'Uploading sweep...',
                                   fg='yellow')) as bar:
            msg_len_bytes = f.read(4)
            while len(msg_len_bytes) > 0:
                msg_len = struct.unpack('I', msg_len_bytes)[0]
                snapshot = proto.Snapshot()
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
                        },
                        'format': 'mind'
                    }
                }
                yield msg
                msg = {
                    'type': 'colorImage',
                    'status': 'uploaded',
                    'userId': user.user_id,
                    'datetime': snapshot.datetime,
                    'data': {
                        'width': snapshot.color_image.width,
                        'height': snapshot.color_image.height,
                        'data': snapshot.color_image.data,
                        'format': 'mind'
                    }
                }
                yield msg
                msg = {
                    'type': 'depthImage',
                    'status': 'uploaded',
                    'tell': f.tell(),
                    'userId': user.user_id,
                    'datetime': snapshot.datetime,
                    'data': {
                        'width': snapshot.depth_image.width,
                        'height': snapshot.depth_image.height,
                        'data': list(snapshot.depth_image.data),
                        'format': 'mind'
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
                        'happiness': snapshot.feelings.happiness,
                        'format': 'mind'
                    }
                }
                yield msg
                bar.update(1)
                msg_len_bytes = f.read(4)
    raise StopIteration()
