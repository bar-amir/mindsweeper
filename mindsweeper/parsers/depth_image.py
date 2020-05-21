import json
from ..utils.parser import Parser

@Parser
def depth_image(request):
    request['status'] = 'parsed'
    return None

if __name__ == '__main__':
    depth_image()