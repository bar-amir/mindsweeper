import bson
import click
import importlib
import sys
from pathlib import Path
from ..utils.config import PROJECT_ROOT


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
