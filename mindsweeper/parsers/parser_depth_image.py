msg_types = {'depthImage'}


def depth_image(msg):
    path = msg['data']['path']
    f = open(path, 'rb')
    print(f.read())
    msg['status'] = 'ready'
    return msg