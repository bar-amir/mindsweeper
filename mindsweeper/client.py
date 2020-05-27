import bson
import click
import requests
from emoji import emojize
from pathlib import Path
from time import sleep
from .readers import Reader


def upload_sample(host='127.0.0.1',
                  port=8000,
                  path=None):
    '''Upload the messages stored in `path` to `host`:`port`.'''
    if not isinstance(host, str):
        raise TypeError("Invalid value for host: not a valid string.")
    if not isinstance(port, int):
        raise TypeError("Invalid value for port: not a valid integer.")
    if not Path(path).exists():
        raise IOError("File does not exist.")
    try:
        reader = Reader(path)
    except ModuleNotFoundError:
        raise IOError("Mindsweeper does not support this file extension. (Reader-function not found)")
        return
    try:
        for msg in reader:
            while True:
                try:
                    response = requests.post(
                        f"http://{host}:{port}/upload", data=bson.encode(msg))
                    if msg['type'] == 'hello' and \
                       response.status_code in [200, 300]:
                        click.echo(click.style('Connection established.', fg='green'))
                        click.echo(click.style('Getting things ready...', fg='yellow'))
                    if response.status_code not in [200, 300]:
                        click.echo(click.style(f'{response.status_code}: {response.text}', fg='red'))
                    break
                except requests.exceptions.ConnectionError:
                    click.echo(click.style('Connection Error. Trying again in 10 seconds.', fg='red'))
                    sleep(10)
    except ModuleNotFoundError:
        raise IOError("Mindsweeper does not support this file extension. (Protobuf module not found)")
        return
    except StopIteration:
        click.echo(click.style(emojize('Uploaded all available data. :ok-hand:'), fg='green'))
        return
    except KeyboardInterrupt:
        click.echo('\nAborted')


@click.group()
def main():
    pass


@main.command(name='upload-sample')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=8000)
@click.argument('path', nargs=1)
def upload_sample_command(host, port, path):
    upload_sample(host=host, port=port, path=path)


if __name__ == '__main__':
    main()
