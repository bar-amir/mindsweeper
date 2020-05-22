import re
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_MESSAGE_QUEUE = 'rabbitmq://127.0.0.1:5672/'
DEFAULT_DATABASE = 'mongodb://localhost:27017/'

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
    PARSERS_DIR = PROJECT_ROOT / 'mindsweeper' / 'parsers'
    parsers = [Path(f.name).stem for f in PARSERS_DIR.iterdir() if f.is_file()]
    parsers.remove('__init__') 
    parsers.remove('__main__')
    return parsers

if __name__ == '__main__':
    print(PROJECT_ROOT)