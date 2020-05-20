from flask import Flask
from flask import send_file
import pymongo
import json
import datetime
from .utils import aux

app = Flask(__name__)

@app.route('/users')
def get_users():
    result = []
    for u in db['users'].find():
        result.append(u)
    return str(result)

@app.route('/snapshots')
def get_snapshots():
    result = []
    for s in db['snapshots'].find():
        result.append(s)
    return str(result)

@app.route('/users/<user_id>')
def get_user(user_id):
    user = db['users'].find_one({'_id': int(user_id)}, {'_id': 0, 'snapshots': 0}) 
    gender = {
        0: 'male',
        1: 'female',
        2: 'other'
    }
    user = {
        'user_id': user_id,
        'username': user['username'],
        'birthday': datetime.datetime.fromtimestamp(user['birthday']).strftime('%Y-%m-%d'),
        'gender:': gender[user['gender']]
    }
    return str(user)

@app.route('/users/<user_id>/snapshots')
def get_user_snapshots(user_id):
    snapshots = db['snapshots'].find({'userId': user_id}, {'_id': 1, 'datetime': 1}).sort('datetime')
    result = []
    for s in snapshots:
        snapshot = {
            'snapshot_id': s['_id'],
            'datetime': datetime.datetime.fromtimestamp(int(s['datetime'])/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
        }
        result.append(snapshot)
    return str(result)

@app.route('/users/<user_id>/snapshots/<snapshot_id>')
def get_user_snapshot(user_id, snapshot_id):
    snapshot = db['snapshots'].find_one({'_id': snapshot_id})
    result = {
        'snapshot_id': snapshot_id,
        'datetime': datetime.datetime.fromtimestamp(int(snapshot['datetime'])/1000).strftime('%Y-%m-%d %H:%M:%S.%f'),
        'results': list(snapshot['results'].keys())
    }
    return str(result)

@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>')
def get_result(user_id, snapshot_id, result_name):
    snapshot = db['snapshots'].find_one({'_id': snapshot_id})
    name = aux.url_to_lower_camel(result_name)
    if name in snapshot['results']:
        result = snapshot['results'][name]
        if name == 'colorImage':
            result['data'] = f"/users/{user_id}/snapshots/{snapshot_id}/{result_name}/data"
            del result['path']
        return str(result)
    else:
        return 'No available data'

@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>/data')
def get_result_data(user_id, snapshot_id, result_name):
    snapshot = db['snapshots'].find_one({'_id': snapshot_id})
    name = aux.url_to_lower_camel(result_name)
    if name in snapshot['results']:
        if name == 'colorImage':
            return send_file(snapshot['results']['colorImage']['path'], mimetype='image/gif')
    else:
        return 'No available data'

def run_api_server(database_url,
                host='127.0.0.1', \
                port=5000):
    '''listen on host:port and serve data from database_url'''
    global client
    global db
    
    client = pymongo.MongoClient(database_url)
    db = client['mindsweeper']
    app.run(host=host, port=port)

if __name__ == '__main__':
    run_api_server('mongodb://localhost:27017/')