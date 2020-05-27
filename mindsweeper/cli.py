'''The CLI module offers command line iterface for consuming the API of Minesweeper, querying its database and printing the results to the console.'''

import click
import requests


@click.group()
def main():
    pass


@main.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=5000)
def get_users(host, port):
    response = requests.get(f"http://{host}:{port}/users")
    click.echo(response.text)


@main.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=5000)
@click.argument('user_id', nargs=1)
def get_user(host, port, user_id):
    response = requests.get(f"http://{host}:{port}/users/{user_id}")
    click.echo(response.text)


@main.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=5000)
@click.argument('user_id', nargs=1)
def get_snapshots(host, port, user_id):
    response = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots")
    click.echo(response.text)


@main.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=5000)
@click.argument('user_id', nargs=1)
@click.argument('snapshot_id', nargs=1)
def get_snapshot(host, port, user_id, snapshot_id):
    response = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}")
    click.echo(response.text)


@main.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=5000)
@click.argument('user_id', nargs=1)
@click.argument('snapshot_id', nargs=1)
@click.argument('result_name', nargs=1)
def get_result(host, port, user_id, snapshot_id, result_name):
    response = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result_name}")
    click.echo(response.text)


if __name__ == '__main__':
    main()
