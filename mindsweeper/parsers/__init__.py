import importlib
import sys
from ..utils import config
import bson


def find_parser(parser_name):
    root = config.PROJECT_ROOT / 'mindsweeper/parsers'
    sys.path.insert(0, str(root))
    name = f'mindsweeper.parsers.parser_{parser_name}'
    importlib.import_module(name, package=root.name)
    func = sys.modules[name].__dict__[parser_name]
    msg_types = sys.modules[name].__dict__['msg_types']
    return func, msg_types