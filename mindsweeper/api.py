import click
import datetime
import json
from flask import Flask, send_file
from flask_cors import CORS, cross_origin
from .drivers import Database
from .utils import aux


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@click.group()
def main():
    pass


@app.route('/users')
@cross_origin()
def get_users():
    collection = db.find('users', {}, {'_id': 1, 'username': 1})
    result = []
    for user in collection:
        # gender = {
        #     0: 'Male',
        #     1: 'Female',
        #     2: 'Other'
        # }
        u = {
            'userId': user['_id'],
            'username': user['username'],
            # 'birthday': datetime.datetime.fromtimestamp(
            #     user['birthday']).strftime('%Y-%m-%d'),
            # 'gender:': gender[user['gender']]
        }
        result.append(u)
    return json.dumps(result)


@app.route('/users/<user_id>/sweeps')
@cross_origin()
def get_sweeps(user_id):
    collection = db.find('sweeps', {'userId': int(user_id)})
    result = []
    for sweep in collection:
        s = {
            'sweepId': sweep['_id'],
            'start': datetime.datetime.fromtimestamp(
                int(sweep['sweepStart'])/1000).strftime(
                    '%Y-%m-%d %H:%M:%S.%f'),
            'end': datetime.datetime.fromtimestamp(
                int(sweep['sweepEnd'])/1000).strftime(
                    '%Y-%m-%d %H:%M:%S.%f'),
            'numOfSnapshots': sweep['numOfSnapshots']
            }
        result.append(s)
    return json.dumps(result)


@app.route('/users/<user_id>/sweeps/<sweep_id>')
@cross_origin()
def get_sweep(user_id, sweep_id):
    sweep = db.find_one('sweeps', {'_id': sweep_id})
    result = {
        'sweepId': sweep['_id'],
        'start': datetime.datetime.fromtimestamp(
            int(sweep['sweepStart'])/1000).strftime(
                '%Y-%m-%d %H:%M:%S.%f'),
        'end': datetime.datetime.fromtimestamp(
            int(sweep['sweepEnd'])/1000).strftime(
                '%Y-%m-%d %H:%M:%S.%f'),
        'numOfSnapshots': sweep['numOfSnapshots']
    }
    return json.dumps(result)


@app.route('/users/<user_id>/sweeps/<sweep_id>/snapshots')
@cross_origin()
def get_sweep_snapshots(user_id, sweep_id):
    sweep = db.find_one('sweeps', {'_id': sweep_id})
    collection = db.find('snapshots', {
        '$and': [{'datetime': {'$gte': sweep['sweepStart']}},
                  {'datetime': {'$lte': sweep['sweepEnd']}}]})
    result = []
    for snapshot in collection:
        s = {
            'snapshotId': snapshot['_id'],
            'datetime': datetime.datetime.fromtimestamp(
                int(snapshot['datetime'])/1000).strftime(
                    '%Y-%m-%d %H:%M:%S.%f'),
            'results': list(snapshot['results'].keys())
        }
        result.append(s)
    return json.dumps(result)


@app.route('/users/<user_id>')
@cross_origin()
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
    return json.dumps(u)


@app.route('/users/<user_id>/snapshots')
@cross_origin()
def get_user_snapshots(user_id):
    collection = db.find('snapshots',
                        {'userId': int(user_id)},
                        {'_id': 1, 'datetime': 1}
                        ).sort('datetime')
    result = []
    for snapshot in collection:
        s = {
            'snapshotId': snapshot['_id'],
            'datetime': datetime.datetime.fromtimestamp(
                int(snapshot['datetime'])/1000).strftime(
                    '%Y-%m-%d %H:%M:%S.%f'),
            # 'results': snapshot['results']
        }
        result.append(s)
    return json.dumps(result)


@app.route('/users/<user_id>/snapshots/<snapshot_id>')
@cross_origin()
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
@cross_origin()
def get_result(user_id, snapshot_id, result_name):
    snapshot = db.find_one('snapshots', {'_id': snapshot_id})
    name = aux.snake_to_lower_camel(result_name, '-')
    if name in snapshot['results']:
        result = snapshot['results'][name]
        if name in ['colorImage', 'depthImage']:
            result['data'] = f"/users/{user_id}/snapshots/{snapshot_id}/{result_name}/data"
            del result['path']
        return json.dumps(result)


@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>/data')
@cross_origin()
def get_result_data(user_id, snapshot_id, result_name):
    snapshot = db.find_one('snapshots', {'_id': snapshot_id})
    name = aux.snake_to_lower_camel(result_name, '-')
    if name in snapshot['results']:
        if name in ['colorImage', 'depthImage']:
            return send_file(
                snapshot['results'][name]['path'], mimetype='image/gif')


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
