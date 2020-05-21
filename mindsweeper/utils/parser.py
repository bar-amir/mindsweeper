import pika
import bson
from . import drivers
from . import aux

def parser_factory(message_queue_url=None):
    print(message_queue_url)
    def parser(function):
        mq = drivers.MessageQueue(message_queue_url)
        mq.start_parser(function)
    return parser