'''A collection of small helpful functions.'''

import re
from pathlib import Path
from . import config
from .. import parsers


def camel_to_snake(name):
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    return name


def snake_to_upper_camel(name, separator='_'):
    name = ''.join(word.title() for word in name.split('_'))
    return name


def snake_to_lower_camel(name, separator='_'):
    name = re.sub(rf'{separator}([a-z])', lambda x: x.group(1).upper(), name)
    return name


def get_interesting_types():
    '''Return a set of all message types that at least one parser
    is interested in.'''
    PARSERS_DIR = config.PROJECT_ROOT / 'mindsweeper/parsers'
    result = set()
    for x in PARSERS_DIR.iterdir():
        if x.name.startswith('parser_'):
            parser_name = x.stem[len('parser_'):]
            _, msg_types = parsers.find_parser(parser_name)
            result = result | msg_types
    return result


def get_parsers_list():
    '''Return a list of available parsers according to their filenames.'''
    PARSERS_DIR = config.PROJECT_ROOT / 'mindsweeper' / 'parsers'
    parsers = [Path(f.name).stem for f in PARSERS_DIR.iterdir() if f.is_file()]
    parsers.remove('__init__')
    parsers.remove('__main__')
    return parsers


def get_parsers():
    '''Return a list of tuples `(parser_name, msg_types)`, where `msg_types`
    is a set of message types that `parser_name` is interested in.'''
    PARSERS_DIR = config.PROJECT_ROOT / 'mindsweeper/parsers'
    result = []
    for f in PARSERS_DIR.iterdir():
        if f.name.startswith('parser_'):
            parser_name = f.stem[len('parser_'):]
            _, msg_types = parsers.find_parser(parser_name)
            result.append((parser_name, msg_types))
    return result


if __name__ == '__main__':
    pass
