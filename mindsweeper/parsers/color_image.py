from PIL import Image
import json
from .parser import Parser
from pathlib import Path

@Parser
def color_image(body):
    body = json.loads(body)
    path = body['path']
    new_path = Path(path).parent.parent / f"{body['datetime']}.png"
    f = open(path, 'rb')
    size = body['width'], body['height']
    image = Image.frombytes('RGB', size, f.read(), 'raw')
    image.save(new_path)
    body[path] = str(new_path)
    return json.dumps(body)

if __name__ == '__main__':
    color_image()