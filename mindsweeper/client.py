from .utils.reader import Reader
import bson
import requests
import click

def upload_sample(host='127.0.0.1', \
                  port=8000, \
                  path=None):
    '''upload path to host:port'''
    reader = Reader(path)
    for msg in reader:
        response = requests.post(f"http://{host}:{port}/upload", data=bson.encode(msg))
    print('Done')

if __name__ == '__main__':
    upload_sample(path='/home/baram/Documents/mindsweeper/sample.mind.gz')