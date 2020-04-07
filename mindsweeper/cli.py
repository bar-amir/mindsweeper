import click

@click.group()
def main():
    pass

if __name__ == '__main__':
    main()

@main.command()
@click.option('-h', '--host', default='127.0.0.1', type=str, help='Host')
@click.option('-p', '--port', default=8000, type=int, help='Port')
@click.argument('path', nargs=1, type=click.Path(exists=True))
def upload_sample(host, port, path):
    """Upload PATH to HOST:PORT."""
    pass

@main.command()
@click.option('-h', '--host', default='127.0.0.1', type=str, help='Host')
@click.option('-p', '--port', default=8000, type=int, help='Port')
@click.argument('publish')
def run_server(host='127.0.0.1', port=8000, publish=None):
    """Listen on HOST:PORT and pass received messages to PUBLISH."""
    pass