'''A collection of functions used to generate messages for testing.'''

from mindsweeper.readers.protos.code import mind_pb2
import time
import struct


def create_pb2_user_msg(length=False):
    user = mind_pb2.User()
    user.user_id = 1
    user.username = 'Bar Amir'
    user.birthday = 747156600
    user.gender = 0
    msg = user.SerializeToString()
    if length:
        msg = struct.pack('I', len(msg)) + msg
    return msg


def create_user_msg():
    return {
        'type': 'user',
        'status': 'uploaded',
        'userId': 1,
        'datetime': int(time.time()),
        'data': {
            'username': 'Bar Amir',
            'birthday': 747156600,
            'gender': 0
        }
    }


def create_pose_msg():
    return {
        'type': 'pose',
        'status': 'uploaded',
        'userId': 1,
        'datetime': int(time.time()),
        'data': {
            'translation': {
                'x': 1.0,
                'y': 1.0,
                'z': 1.0,
            },
            'rotation': {
                'x': 1.0,
                'y': 1.0,
                'z': 1.0,
                'w': 1.0
            }
        }
    }


def create_color_image_msg():
    return {
        'type': 'colorImage',
        'status': 'uploaded',
        'userId': 1,
        'datetime': int(time.time()),
        'data': {
            'width': 496351,
            'height': 1,
            'data': 'fake-data'.encode()
        }
    }
