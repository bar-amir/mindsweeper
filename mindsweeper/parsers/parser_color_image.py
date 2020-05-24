import click
from PIL import Image
from pathlib import Path
import os

msg_types = {'colorImage'}


def color_image(msg):
    '''
    Receives a colorImage message.
    Parses the binary file at path to a png file, deletes
    the binary file, and updates the message with the path
    to the image.
    '''
    path = msg['data']['path']
    f = open(path, 'rb')
    size = msg['data']['width'], msg['data']['height']
    image = Image.frombytes('RGB', size, f.read(), 'raw')
    new_path = Path(path).parent.parent / f"{msg['datetime']}.png"
    image.save(new_path)
    os.remove(path)
    click.echo(f'Saved image to {new_path}')
    msg['data']['path'] = str(new_path)
    msg['status'] = 'ready'
    return msg
