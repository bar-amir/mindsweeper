import json
from .parser import Parser

@Parser
def feelings(request):
    request = json.loads(request)
    msg = {
        'type': 'feelings',
        'userId': request['userId'],
        'datetime': request['datetime'],
        'data': {}
    }
    for k in request:
        if k != 'userId' and k != 'datetime':
            msg['data'][k] = request[k]
    msg = json.dumps(msg)
    return msg

if __name__ == '__main__':
    feelings()