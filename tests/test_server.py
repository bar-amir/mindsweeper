import pytest
from click.testing import CliRunner
from mindsweeper import server


def test_client_error(tmp_path):
    with pytest.raises(TypeError):
        server.run_server(host=1)
        server.run_server(port='string')
        server.run_server(publish=1)