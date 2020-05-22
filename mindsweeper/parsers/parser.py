import pika
import bson
from . import drivers
from . import aux


def parser_factory(message_queue_url=None, msg_types):
    def parser(function):
        mq = drivers.MessageQueue(message_queue_url)
        mq.start_parser(function, msg_types)
    return parser
