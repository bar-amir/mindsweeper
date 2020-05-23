from flask import Flask, send_file
import json
import datetime
from .utils import aux
import click
from .drivers import Database

app = Flask(__name__)


@click.group()
def main():
    pass


@app.route('/users')
def get_users():
    collection = db.find('users', {}, {'_id': 1, 'username': 1})
    return json.dumps(list(collection))


@app.route('/users/<user_id>/sweeps')
def get_sweeps(user_id):
    collection = db.find('sweeps', {'userId': int(user_id)})
    return json.dumps(list(collection))


@app.route('/users/<user_id>/sweeps/<sweep_id>/snapshots')
def get_sweep_snapshots(user_id, sweep_id):
    sweep = db.find_one('sweeps', {'_id': sweep_id})
    print(sweep)
    collection = db['snapshots'].find(
        {'$and': [{'datetime': {'$gte': sweep['sweepStart']}},
                  {'datetime': {'$lte': sweep['sweepEnd']}}]})
    return json.dumps(list(collection))


@app.route('/users/<user_id>')
def get_user(user_id):
    user = db.find_one('users', {'_id': int(user_id)}, {'snapshots': 0})
    gender = {
        0: 'Male',
        1: 'Female',
        2: 'Other'
    }
    u = {
        'userId': user['_id'],
        'username': user['username'],
        'birthday': datetime.datetime.fromtimestamp(
            user['birthday']).strftime('%Y-%m-%d'),
        'gender:': gender[user['gender']]
    }
    print(u)
    return json.dumps(u)


@app.route('/users/<user_id>/snapshots')
def get_user_snapshots(user_id):
    snapshots = db.find('snapshots',
                        {'userId': int(user_id)},
                        {'_id': 1, 'datetime': 1}).sort('datetime')
    result = []
    for s in snapshots:
        result.append(s)
    return json.dumps(result)


@app.route('/users/<user_id>/snapshots/<snapshot_id>')
def get_user_snapshot(user_id, snapshot_id):
    snapshot = db.find_one('snapshots', {'_id': snapshot_id})
    result = {
        'snapshotId': snapshot['_id'],
        'datetime': datetime.datetime.fromtimestamp(
            int(snapshot['datetime'])/1000).strftime(
                '%Y-%m-%d %H:%M:%S.%f'),
        'results': list(snapshot['results'].keys())
    }
    return json.dumps(result)


@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>')
def get_result(user_id, snapshot_id, result_name):
    snapshot = db.find_one('snapshots', {'_id': snapshot_id})
    name = aux.snake_to_lower_camel(result_name, '-')
    if name in snapshot['results']:
        result = snapshot['results'][name]
        if name in ['colorImage', 'depthImage']:
            result['data'] = f"/users/{user_id}/snapshots/{snapshot_id}/{result_name}/data"
            del result['path']
        return json.dumps(result)
    else:
        return 'No available data'


@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>/data')
def get_result_data(user_id, snapshot_id, result_name):
    snapshot = db.find_one('snapshots', {'_id': snapshot_id})
    name = aux.snake_to_lower_camel(result_name, '-')
    if name in snapshot['results']:
        if name in ['colorImage', 'depthImage']:
            return send_file(
                snapshot['results'][name]['path'], mimetype='image/gif')
    else:
        return 'No available data'


def run_api_server(database_url,
                   host='127.0.0.1',
                   port=5000):
    '''listen on host:port and serve data from database_url'''
    global db
    db = Database(database_url)
    app.run(host=host, port=port)


@main.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=5000)
@click.option('-d', '--database')
def run_server(host='127.0.0.1', port=5000, database=None):
    run_api_server(database, host, port)


if __name__ == '__main__':
    main()
