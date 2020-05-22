msg_types = {'feelings'}


def feelings(msg):
    msg['status'] = 'ready'
    return msg
