import re
from pathlib import Path
from .. import config


def camel_to_snake(name):
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    return name


def snake_to_upper_camel(name, separator='_'):
    name = ''.join(word.title() for word in name.split('_'))
    return name


def snake_to_lower_camel(name, separator='_'):
    name = re.sub(rf'{separator}([a-z])', lambda x: x.group(1).upper(), name)
    return name


def get_parsers_list():
    PARSERS_DIR = config.PROJECT_ROOT / 'mindsweeper' / 'parsers'
    parsers = [Path(f.name).stem for f in PARSERS_DIR.iterdir() if f.is_file()]
    parsers.remove('__init__')
    parsers.remove('__main__')
    return parsers
