import json
from ..utils.parser import Parser

@Parser
def pose(request):
    request = json.loads(request)
    msg = {
        'type': 'pose',
        'userId': request['userId'],
        'datetime': request['datetime'],
        'data': {
            'translation': request['translation'],
            'rotation': request['rotation']
        }
    }
    msg = json.dumps(msg)
    return msg

if __name__ == '__main__':
    pose()