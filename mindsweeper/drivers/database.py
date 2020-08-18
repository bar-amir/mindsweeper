import traceback
from .databases import MongoDB
from ..utils.config import DEFAULT_DATABASE

drivers = {'mongodb://': MongoDB}


class Database:
    def __init__(self, url):
        if not url:
            url = DEFAULT_DATABASE
        self.driver = find_driver(url)

    def upsert(self, msg):
        t = msg['type']
        try:
            if t == 'user':
                self.driver.upsert_user(msg)
            elif t == 'sweep':
                self.driver.upsert_sweep(msg)
            elif t in ['colorImage', 'depthImage', 'pose', 'feelings']:
                self.driver.upsert_result(msg)
            else:
                raise ValueError(
                    f"Database does not support message type {t}")
            print(f"Created new entry {msg['type']}")
        except Exception:
            traceback.print_exc()

    def find(self, collection, query, projection=None):
        return self.driver.find(collection, query, projection)

    def find_one(self, collection, query, projection=None):
        return self.driver.find_one(collection, query, projection)


def find_driver(url):
    for scheme, cls in drivers.items():
        if url.startswith(scheme):
            return cls(url)
    raise ValueError(f'invalid url: {url}')
