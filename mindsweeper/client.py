import requests
import bson
import click
from emoji import emojize
from .readers import Reader


@click.group()
def main():
    pass


@main.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=8000)
@click.argument('path', nargs=1)
def upload_sample(host='127.0.0.1',
                  port=8000,
                  path=None):
    '''upload path to host:port'''
    reader = Reader(path)
    for msg in reader:
        response = requests.post(f"http://{host}:{port}/upload", data=bson.encode(msg))


if __name__ == '__main__':
    main()