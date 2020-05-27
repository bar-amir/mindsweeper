import click
import os
from .utils.config import PROJECT_ROOT


def create_env(host='127.0.0.1',
               port=8080,
               api_host='127.0.0.1',
               api_port=5000):
    with open(PROJECT_ROOT / 'mindsweeper/gui/.env', 'w+') as f:
        f.write(f'HOST={host} \n' +
                f'PORT={port} \n' +
                f'REACT_APP_API_HOST={api_host}\n' +
                f'REACT_APP_API_PORT={api_port}')


def run_server(host='127.0.0.1',
               port=8080,
               api_host='127.0.0.1',
               api_port=5000):
    create_env(host, port, api_host, api_port)
    os.system('cd mindsweeper/gui && npm start')


@click.group()
def main():
    pass


@main.command(name='create-env')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=8080)
@click.option('-H', '--api-host', default='127.0.0.1')
@click.option('-P', '--api-port', default=5000)
def create_env_command(host, port, api_host, api_port):
    create_env(host=host,
               port=port,
               api_host=api_host,
               api_port=api_port)


@main.command(name='run-server')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=8080)
@click.option('-H', '--api-host', default='127.0.0.1')
@click.option('-P', '--api-port', default=5000)
def run_server_command(host, port, api_host, api_port):
    run_server(host=host,
               port=port,
               api_host=api_host,
               api_port=api_port)


if __name__ == '__main__':
    main()
