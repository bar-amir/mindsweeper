from PIL import Image
import json
from .parser import Parser
from pathlib import Path

@Parser
def color_image(request):
    request = json.loads(request)
    path = request['data']['path']
    f = open(path, 'rb')
    size = request['data']['width'], request['data']['height']
    image = Image.frombytes('RGB', size, f.read(), 'raw')
    new_path = Path(path).parent.parent / f"{request['datetime']}.png"
    image.save(new_path)
    request['data']['path'] = str(new_path)
    msg = json.dumps(request)
    return msg

if __name__ == '__main__':
    color_image()