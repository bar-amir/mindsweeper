from .message_queues import RabbitMQ
from ..utils.config import DEFAULT_MESSAGE_QUEUE

drivers = {'rabbitmq://': RabbitMQ}


class MessageQueue:
    def __init__(self, url):
        if not url:
            url = DEFAULT_MESSAGE_QUEUE
        self.driver = find_driver(url)

    def publish(self, msg):
        self.driver.publish(msg)

    def start_parser(self, function, msg_types):
        self.driver.start_parser(function, msg_types)

    def start_saver(self, function):
        self.driver.start_saver(function)

    def close(self):
        self.driver.close()


def find_driver(url):
    for scheme, cls in drivers.items():
        if url.startswith(scheme):
            return cls(url)
    raise ValueError(f'Invalid URL: {url}')
