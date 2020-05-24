
import bson
import click
from . import find_parser
from ..drivers import MessageQueue


@click.group()
def main():
    pass


def run_parser(parser_name, message_queue_url=None):
    parser_func, msg_types = find_parser(parser_name)
    mq = MessageQueue(message_queue_url)
    mq.start_parser(parser_func, msg_types)


@main.command(name='run-parser')
@click.argument('parser_name', nargs=1)
@click.argument('message_queue_url', nargs=1)
def run_parser_command(parser_name, message_queue_url):
    run_parser(parser_name=parser_name,
               message_queue_url=message_queue_url)


@main.command()
@click.argument('parser_name', nargs=1)
@click.argument('path', nargs=1, default=None)
def parse(parser_name, path):
    parser, msg_types = find_parser(parser_name)
    with open(path, 'rb') as f:
        data = bson.decode(f.read())
        if data['type'] not in msg_types:
            raise ValueError(f'Data incompatible with parser {parser_name}')
        click.echo(parser(data))


if __name__ == '__main__':
    main()
