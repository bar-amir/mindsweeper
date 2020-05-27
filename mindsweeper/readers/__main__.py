import click
from . import read_to_files


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
