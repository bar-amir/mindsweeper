
import bson
from . import *
from ..drivers import MessageQueue


def run_parser(parser_name, message_queue_url=None):
    '''Connect to message queue and start the parser as a service.'''
    parser_func, msg_types = find_parser(parser_name)
    if not parser_func and not msg_types:
        raise ModuleNotFoundError('Parser-function not found.')
    mq = MessageQueue(message_queue_url)
    mq.start_parser(parser_func, msg_types)


@click.group()
def main():
    pass


@main.command(name='run-parser')
@click.argument('parser_name', nargs=1)
@click.argument('message_queue_url', nargs=1)
def run_parser_command(parser_name, message_queue_url):
    run_parser(parser_name=parser_name,
               message_queue_url=message_queue_url)


@main.command(name='parse')
@click.argument('parser_name', nargs=1)
@click.argument('path', nargs=1, default=None)
def parse_command(parser_name, path):
    msg = parse(parser_name=parser_name, path=path)
    return bson.encode(msg)


if __name__ == '__main__':
    main()
