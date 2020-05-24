import sys
from importlib import import_module
from pathlib import Path
from ..utils.config import PROJECT_ROOT


class Reader:
    '''
    Convert to JSON messages stored in `path` and iterates through them.
    Readers use reader-functions to handle the file in `path`.
    Each reader-function handles a different file format,
    which it identifies according to the file's extension.
    '''
    def __init__(self, path):
        reader_func = find_reader(path)
        if not reader_func:
            raise ModuleNotFoundError('Reader-function not found.')
        self.gen = reader_func(path)

    def __iter__(self):
        yield {'type': 'hello'}
        while True:
            try:
                yield from self.gen
            except StopIteration as e:
                raise e


def proto_reader(func):
    '''
    Used to decorate reader-functions that reads protobuf files.
    These reader functions could assist `_pb2.py` files, generated
    by the gRPC module.
    '''
    def wrapper(path):
        proto_module = find_proto_module(func.__name__)
        return func(path, proto_module)
    return wrapper


def find_proto_module(fmt):
    '''
    Return module generated for handling `fmt` protobufs.
    Returns `None` if not found
    '''
    root = PROJECT_ROOT / 'mindsweeper/readers/protos/code'
    sys.path.insert(0, str(root))
    name = f'mindsweeper.readers.protos.code.{fmt}_pb2'
    try:
        import_module(name, package=root.name)
    except ModuleNotFoundError:
        return None
    proto_module = sys.modules[name]
    return proto_module


def find_reader(path):
    '''
    Return the reader-function that reads `path`.
    Returns `None` if not found.
    '''
    fmt, *ext = Path(path).suffixes
    fmt = fmt[1:]
    root = PROJECT_ROOT / 'mindsweeper/readers'
    sys.path.insert(0, str(root))
    name = f'mindsweeper.readers.reader_{fmt}'
    try:
        import_module(name, package=root.name)
    except ModuleNotFoundError:
        return None
    return sys.modules[name].__dict__[fmt]
