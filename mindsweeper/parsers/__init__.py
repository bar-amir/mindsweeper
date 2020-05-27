'''This module offers methods to use parsers in various ways, and a framework for implementing your own parsers.
'''

import bson
import click
from pathlib import Path
from ..drivers import MessageQueue
from ..utils.aux import find_parser


def run_parser(parser_name, message_queue_url=None):
    '''Connect to message queue and start the parser as a service.'''
    parser_func, msg_types = find_parser(parser_name)
    if not parser_func and not msg_types:
        raise ModuleNotFoundError('Parser-function not found.')
    mq = MessageQueue(message_queue_url)
    mq.start_parser(parser_func, msg_types)


def parse(parser_name, path):
    '''Parses the data found in the file `path` with the parser `parser_name` (string).'''
    if not Path(path).exists():
        raise IOError("File does not exist.")
    parser, msg_types = find_parser(parser_name)
    with open(path, 'rb') as f:
        data = bson.decode(f.read())
        if data['type'] not in msg_types:
            raise ValueError(f'Data incompatible with parser {parser_name}')
        click.echo(parser(data))
        return parser(data)
