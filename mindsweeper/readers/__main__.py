import bson
import click
import os
import time
from . import Reader
from ..utils.config import PROJECT_ROOT


def read_to_files(path, output=None,):
    if not output:
        output = PROJECT_ROOT / 'tests' / 'messages'
    reader = Reader(path)
    os.makedirs(output, exist_ok=True)
    for msg in reader:
        name = f"{msg['type']}-{str(int(time.time()))}.dat"
        with open(output / name, 'wb') as f:
            f.write(bson.encode(msg))
        click.echo(f'Wrote message to {output / name}.')


@click.group()
def main():
    pass


@main.command(name='read-to-files')
@click.argument('path', nargs=1)
@click.option('-o', '--output', nargs=1, default=None)
def read_to_files_command(path, output):
    read_to_files(path=path, output=output)


if __name__ == '__main__':
    main()
