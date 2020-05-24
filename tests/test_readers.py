import pytest
from mindsweeper import readers
from mindsweeper.readers.protos.code import mind_pb2


def create_user_message():
    user = mind_pb2.User()
    user.user_id = 1
    user.username = 'Bar Amir'
    user.birthday = 747156600
    user.gender = 0
    msg = user.SerializeToString()
    msg_len = struct.pack('I', len(msg))
    return 


def create_snapshot():
    snapshot = mind_pb2.Snapshot()
    pose = mind_pb2.Pose
    translation = mind_pb2.Pose().Translation()
    rotation = mind_pb2.Pose().Rotation()
    color_image = mind_pb2.ColorImage()
    depth_image = mind_pb2.DepthImage()
    feelings = mind_pb.Feelings()


def test_mind_reader(tmp_path)
    pass


def test_reader(tmp_path):
    f = tmp_path / 'file'


def test_finds():
    proto = readers.find_proto_module('unsupported')
    assert proto is None
    proto = readers.find_proto_module('mind')
    assert proto is not None
    reader = readers.find_reader('file.unsupported')
    assert reader is None
    reader = readers.find_reader('file.unsupported.gz')
    assert reader is None
    reader = readers.find_reader('file.mind')
    assert reader is not None
    reader = readers.find_reader('file.mind.gz')
    assert reader is not None


def test_readers_error(tmp_path):
    # f = tmp_path / 'file.txt'
    # with pytest.raises(TypeError):
    #     client.upload_sample(host=1)
    #     client.upload_sample(port='string')
    # with pytest.raises(IOError):
    #     client.upload_sample(path=tmp_path / 'file.unsupported.format')
    #     client.upload_sample(path=f)
    pass
