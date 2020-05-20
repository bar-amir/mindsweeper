import json
from .parser import Parser

@Parser
def depth_image(request):
    request = json.loads(request)

if __name__ == '__main__':
    depth_image()