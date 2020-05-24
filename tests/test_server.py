import bson
import shutil
import pytest
import requests
from . import msg_gen as mg
from click.testing import CliRunner
from mindsweeper import server
from mindsweeper.utils import aux
from pathlib import Path


HOST = '127.0.0.1'
PORT = 8000


def test_server_error(tmp_path):
    with pytest.raises(TypeError):
        server.run_server(host=1)
        server.run_server(port='string')
        server.run_server(publish=1)


def upload(msg):
    def publish(msg):
        return
    response = server.upload(msg, publish)
    assert response == 'OK'
    if msg['type'] in aux.get_interesting_types():
        assert msg['status'] == 'unparsed'
    else:
        assert msg['status'] == 'ready'
    if msg['type'] in ['colorImage', 'depthImage']:
        path = Path(msg['data']['path'])
        assert path.exists()
        shutil.rmtree(path.parent)
    assert response == 'OK'


def test_upload_user_msg():
    upload(mg.create_user_msg())

def test_upload_color_image_msg():   
    upload(mg.create_color_image_msg())

def test_upload_pose_msg():
    upload(mg.create_pose_msg())
