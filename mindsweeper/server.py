from .drivers import MessageQueue
import bson
import struct
import click
import os
from flask import Flask, request
from .utils import aux, config

app = Flask(__name__)


@click.group()
def main():
    pass


@main.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=8000)
@click.argument('message_queue_url', nargs=1, default=None)
def run_server(host='127.0.0.1',
               port=8000,
               publish=None,
               message_queue_url=None):
    '''listen on host:port and pass received messages to publish'''
    global publish_func
    mq = MessageQueue(message_queue_url)
    if not publish:
        publish_func = mq.publish
    else:
        publish_func = publish
    app.run(host=host, port=port)
    # mq.close()


@app.route('/upload', methods=['POST'])
def upload():
    msg = bson.decode(request.get_data())
    if msg['type'] in ['colorImage', 'depthImage']:
        if msg['type'] == 'depthImage':
            floatlist = msg['data']['data']
            msg['data']['dataLen'] = len(floatlist)
            msg['data']['data'] = struct.pack(
                '%sf' % len(floatlist), *floatlist)
        dir_name = aux.camel_to_snake(msg['type'])
        dir_path = config.PROJECT_ROOT / f"media/{dir_name}s/{str(msg['userId'])}/bin"
        file_path = dir_path / f"{msg['datetime']}.dat"
        os.makedirs(dir_path, exist_ok=True)
        f = open(file_path, 'wb')
        f.write(msg['data']['data'])
        del msg['data']['data']
        msg['data']['path'] = str(file_path)
        f.close()
    if msg['type'] in aux.get_interesting_types():
        msg['status'] = 'unparsed'
    else:
        msg['status'] = 'ready'
    publish_func(msg)
    return 'OK'


if __name__ == '__main__':
    main()
