import json
from ..utils.parser import Parser

@Parser
def feelings(request):
    print(request)
    return request

if __name__ == '__main__':
    feelings()