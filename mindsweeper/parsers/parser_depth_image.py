import echo
import os
from pathlib import Path
import struct
import numpy
import seaborn
import matplotlib.pyplot as plt


msg_types = {'depthImage'}


def depth_image(msg):
    path = msg['data']['path']
    f = open(path, 'rb')
    size = msg['data']['height'], msg['data']['width']
    values = struct.unpack(
                '%sf' % msg['data']['dataLen'], f.read())
    del msg['data']['dataLen']
    values = numpy.reshape(values, size)
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ax = seaborn.heatmap(values,
                         cmap='plasma_r')
    new_path = Path(path).parent.parent / f"{msg['datetime']}.png"
    plt.savefig(new_path, transparent=True)
    plt.clf()
    os.remove(path)
    click.echo(f'Saved image to {new_path}')
    msg['data']['path'] = str(new_path)
    msg['status'] = 'ready'
    return msg
