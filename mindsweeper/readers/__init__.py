import click
import importlib
from pathlib import Path
import sys
from ..utils import config
from emoji import emojize


class Reader:
    def __init__(self, path):
        reader = find_reader(path)
        self.gen = reader(path)

    def __iter__(self):
        try:
            yield from self.gen
        except StopIteration:
            click.echo(click.style(emojize(
                'Uploaded all available data. Goodbye. :waving_hand:'),
                fg='green'))


def find_reader(path):
    fmt, *ext = Path(path).suffixes
    fmt = fmt[1:]
    root = config.PROJECT_ROOT / 'mindsweeper/readers'
    sys.path.insert(0, str(root))
    name = f'mindsweeper.readers.reader_{fmt}'
    importlib.import_module(name, package=root.name)
    return sys.modules[name].__dict__[fmt]


def find_proto_module(fmt):
    '''Returns the module generated for file extension'''
    root = config.PROJECT_ROOT / 'mindsweeper/readers/protos/code'
    sys.path.insert(0, str(root))
    name = f'mindsweeper.readers.protos.code.{fmt}_pb2'
    importlib.import_module(name, package=root.name)
    return sys.modules[name]


def proto_reader(func):
    def wrapper(path):
        proto = find_proto_module(func.__name__)
        return func(path, proto)
    return wrapper
