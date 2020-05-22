msg_types = {'pose'}


def pose(msg):
    msg['status'] = 'ready'
    return msg
