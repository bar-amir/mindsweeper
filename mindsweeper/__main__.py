import click
import server

@click.command()
@click.option('--address', help='Address')
@click.option('--data', help='Data')
def run(address, data):
    """"""
    server.run(address, data)

if __name__ == '__main__':
    run()
