import bson
from click.testing import CliRunner
from . import msg_gen as mg
from mindsweeper import parsers


HOST = '127.0.0.1'
PORT = 8000


def test_parse(tmp_path):
    path = tmp_path / 'raw.bin'
    with open(path, 'wb') as f:
        msg = mg.create_pose_msg()
        f.write(bson.encode(msg))
    msg = parsers.parse('pose', path)
    assert msg['status'] == 'ready'

