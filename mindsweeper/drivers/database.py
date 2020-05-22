from .databases import MongoDB

drivers = {'mongodb://'}


class Database:
    def __init__(self, url):
        self.driver = find_driver(url)

    def create_user(self, **kwargs):
        pass

    def get_user(self, **kwargs):
        pass

    def update_user(self, **kwargs):
        pass

    def create_sweep(self, **kwargs):
        pass

    def get_sweep(self, **kwargs):
        pass

    def update_sweep(self, **kwargs):
        pass

    def create_snapshot(self, **kwargs):
        pass

    def get_snapshot(self, **kwargs):
        pass

    def update_snapshot(self, **kwargs):
        pass


def find_driver(url):
    for scheme, cls in drivers.items():
        if url.startswith(scheme):
            return cls(url)
    raise ValueError(f'invalid url: {url}')
