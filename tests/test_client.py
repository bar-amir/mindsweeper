import pytest
from mindsweeper import client


def test_client_error(tmp_path):
    f = tmp_path / 'file.txt'
    with pytest.raises(TypeError):
        client.upload_sample(host=1)
        client.upload_sample(port='string')
    with pytest.raises(IOError):
        client.upload_sample(path=tmp_path / 'file.unsupported.format')
        client.upload_sample(path=f)
