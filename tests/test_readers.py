from mindsweeper import readers


def test_reader(tmp_path):
    pass


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
