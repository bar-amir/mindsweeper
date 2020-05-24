import pytest
from mindsweeper import readers
from mindsweeper.readers.protos.code import mind_pb2





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
