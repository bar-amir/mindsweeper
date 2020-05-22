from .utils import drivers, aux
import bson
import click
import os
from concurrent import futures
from pathlib import Path
from flask import Flask, request

app = Flask(__name__)

@click.group()
def main():
    pass

@main.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=8000)
@click.argument('message_queue_url', nargs=1, default=None)
def run_server(host='127.0.0.1', \
               port=8000, \
               publish=None, \
               message_queue_url=None):
    '''listen on host:port and pass received messages to publish'''
    global mq
    global publish_func
    mq = drivers.MessageQueue(message_queue_url)
    if not publish:
        publish_func = mq.publish
    else:
        publish_func = publish
    app.run(host=host, port=port)
    mq.close()

length = 0

@app.route('/upload', methods=['POST'])
def upload():
    msg = bson.decode(request.get_data())
    msg['type'] = aux.camel_to_snake(msg['type'])

    if msg['type'] in ['color_image']:
        dir_path = aux.PROJECT_ROOT / 'media' / 'color_images' / str(msg['userId']) / 'bin'
        file_path = dir_path / f"{msg['datetime']}.dat"
        os.makedirs(dir_path, exist_ok=True)
        f = open(file_path, 'wb+')
        f.write(msg['data']['data'])
        del msg['data']['data']
        msg['data']['path'] = str(file_path)

    if msg['type'] in aux.get_parsers_list():
        msg['status'] = 'unparsed'

    publish_func(msg)
    return 'OK'


if __name__ == '__main__':
    main()
    