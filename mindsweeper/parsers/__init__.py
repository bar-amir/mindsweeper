import bson
import click
import importlib
import sys
from pathlib import Path
from ..drivers import MessageQueue
from ..utils.config import PROJECT_ROOT


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


def find_parser(parser_name):
    '''
    Returns:
        func (function): The parser-function `parser_name`, found in 'parser_`parser_name`.py'.
        msg_types (set): `func`'s `msg_types`, i.e. the messages this parser-function handles.
    '''
    root = PROJECT_ROOT / 'mindsweeper/parsers'
    sys.path.insert(0, str(root))
    name = f'mindsweeper.parsers.parser_{parser_name}'
    try:
        importlib.import_module(name, package=root.name)
        func = sys.modules[name].__dict__[parser_name]
        msg_types = sys.modules[name].__dict__['msg_types']
    except ModuleNotFoundError:
        return None, None
    return func, msg_types


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
    parse(parser_name=parser_name, path=path)
