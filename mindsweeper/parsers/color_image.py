from PIL import Image
from ..utils.parser import Parser
from pathlib import Path

@Parser
def color_image(request):
    path = request['data']['path']
    f = open(path, 'rb')
    size = request['data']['width'], request['data']['height']
    image = Image.frombytes('RGB', size, f.read(), 'raw')
    new_path = Path(path).parent.parent / f"{request['datetime']}.png"
    image.save(new_path)
    os.remove(path)
    print(f' [X] Saved image to {new_path}')
    request['data']['path'] = str(new_path)
    request['status'] = 'parsed'
    return request

if __name__ == '__main__':
    color_image()