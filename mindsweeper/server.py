'''Server'''

import bson
import click
import os
import struct
from flask import Flask, request
from .utils import aux
from .utils.config import PROJECT_ROOT
from .drivers import MessageQueue

app = Flask(__name__)


def run_server(host='127.0.0.1',
               port=8000,
               publish=None):
    '''Listen on `host`:`port` and pass received messages to `publish`.'''
    if not isinstance(host, str):
        raise TypeError("Invalid value for host: not a valid string.")
    if not isinstance(port, int):
        raise TypeError("Invalid value for port: not a valid integer.")
    if publish and not callable(publish):
        raise TypeError("Invalid value for func: not callable.")
    global publish_func
    if not publish:
        click.echo("Error: Missing argument 'publish'")
        return
    else:
        publish_func = publish
    app.run(host=host, port=port)


def upload(msg, publish):
    '''
    Receives a message in a format readable by the server,
    and make it ready to be sent to the message queue:
    Messages with types mentioned in any parser's `msg_types`,
    will change their status to 'unparsed'.
    Other messages will change their status to 'ready'.
    For messages with large amount of data (like images),
    their data should be saved to a reasonable path under the
    'media' folder.
    '''
    if msg['type'] == 'hello':  # a little handshake with client
        return 'HELLO'
    if msg['type'] in ['colorImage', 'depthImage']:
        if msg['type'] == 'depthImage':
            floatlist = msg['data']['data']
            msg['data']['dataLen'] = len(floatlist)
            msg['data']['data'] = struct.pack(
                '%sf' % len(floatlist), *floatlist)
        dir_name = aux.camel_to_snake(msg['type'])
        dir_path = PROJECT_ROOT / f"media/{dir_name}s/{str(msg['userId'])}/bin"
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
    publish(msg)
    return 'OK'
    

@click.group()
def main():
    pass


@main.command(name='run-server')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=8000)
@click.argument('message_queue_url', nargs=1, default=None)
def run_server_command(host, port, message_queue_url):
    global publish_func
    mq = MessageQueue(message_queue_url)
    publish_func = mq.publish
    app.run(host=host, port=port)
    # mq.close()


@app.route('/upload', methods=['POST'])
def upload_api():
    '''Flask API - All upload requests will go through this url.'''
    return upload(bson.decode(request.get_data()), publish_func)


if __name__ == '__main__':
    main()
