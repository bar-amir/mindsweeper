import click
import importlib
import sys
from pathlib import Path
from ..utils.parser import parser_factory
from ..utils import aux
from inspect import getmembers
import bson

@click.group()
def main():
    pass

def find_parser(parser_name):
    root = aux.PROJECT_ROOT / 'mindsweeper' / 'parsers'
    sys.path.insert(0, str(root))
    #module_name = f'mindsweeper.parsers.{parser_name}'
    importlib.import_module(parser_name, package=root.name)
    parser = sys.modules[parser_name].__dict__[parser_name]
    return parser

@main.command()
@click.argument('parser_name', nargs=1)
@click.argument('message_queue_url', nargs=1, default=None)
def run_parser(parser_name, message_queue_url=None):
    parser = find_parser(parser_name)
    parser_factory(message_queue_url)(parser)() 

@main.command()
@click.argument('parser_name', nargs=1)
@click.argument('path', nargs=1, default=None)
def parse(parser_name, path):
    parser = find_parser(parser_name)
    with open(path,'rb') as f:
        data = bson.decode(f.read())
        click.echo(parser(data))

if __name__ == '__main__':
    main()
