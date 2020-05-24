import click

@click.group()
def main():
    pass


def run_server(host='127.0.0.1', port=8080, api_host='127.0.0.1', api_port=5000):
    pass


@click.command(name='run-server')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-h', '--port', default=8080)
@click.option('-H', '--api-host', default='127.0.0.1')
@click.option('-P', '--api-port', default=5000)
def run_server_command(host, port, api_host, api_port):
    run_server(host=host,
               port=port,
               api_host=api_host,
               api_port=api_port)


if __name__ == '__main__':
    main()
