from urllib.parse import urlparse
from mindsweeper.drivers import message_queue as mq
from mindsweeper.drivers import database as db
from mindsweeper.utils import config


def test_mq_default():
    drivers = mq.drivers
    result = urlparse(config.DEFAULT_MESSAGE_QUEUE)
    assert f'{result.scheme}://' in drivers, 'default message queue driver is not supported.'


def test_db_default():
    drivers = db.drivers
    result = urlparse(config.DEFAULT_DATABASE)
    assert f'{result.scheme}://' in drivers, 'default database driver is not supported.'
