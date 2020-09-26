'''This module contains methods for running and API server and querying the database with it. Queries are implemented in the format of MongoDB queries, the default database of Mindsweeper, although other drivers can be implemented. The response of successful queries are in JSON format.
'''

import click
import datetime
import json
from flask import Flask, send_file
from flask_cors import CORS, cross_origin
from .drivers.database import Database
from .utils import auxiliary


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@click.group()
def main():
    pass


@app.route('/users')
@cross_origin()
def get_users():
    '''Return a list of all users at `/users`.'''
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
    '''Return a list of all of `<user_id>`'s sweeps at `/users/<user_id>/sweeps`.'''
    collection = db.find('sweeps', {'userId': int(user_id)})
    result = []
    for sweep in collection:
        start_obj = datetime.datetime.fromtimestamp(
                int(sweep['sweepStart'])/1000)
        end_obj = datetime.datetime.fromtimestamp(
                int(sweep['sweepEnd'])/1000)
        s = {
            'sweepId': sweep['_id'],
            'start': start_obj.strftime(
                    '%Y-%m-%d %H:%M:%S.%f'),
            'end': end_obj.strftime(
                    '%Y-%m-%d %H:%M:%S.%f'),
            'numOfSnapshots': sweep['numOfSnapshots'],
            'name': sweep['name'],
            'startDate': datetime.datetime.strftime(start_obj, "%Y-%m-%d"),
            'startTime': datetime.datetime.strftime(start_obj, "%I:%M %p"),
            'duration': str(end_obj - start_obj).split('.')[0],
            }
        result.append(s)
    return json.dumps(result)


@app.route('/users/<user_id>/sweeps/<sweep_id>')
@cross_origin()
def get_sweep(user_id, sweep_id):
    '''Return the sweep `sweep_id  of the user `user_id` at `/users/<user_id>/sweeps/<sweep_id>`.'''
    sweep = db.find_one('sweeps', {'_id': sweep_id})
    start_obj = datetime.datetime.fromtimestamp(
                int(sweep['sweepStart'])/1000)
    end_obj = datetime.datetime.fromtimestamp(
            int(sweep['sweepEnd'])/1000)
    result = {
        'sweepId': sweep['_id'],
        'start': datetime.datetime.fromtimestamp(
            int(sweep['sweepStart'])/1000).strftime(
                '%Y-%m-%d %H:%M:%S.%f'),
        'end': datetime.datetime.fromtimestamp(
            int(sweep['sweepEnd'])/1000).strftime(
                '%Y-%m-%d %H:%M:%S.%f'),
        'numOfSnapshots': sweep['numOfSnapshots'],
        'name': sweep['name'],
        'startDate': datetime.datetime.strftime(start_obj, "%Y-%m-%d"),
        'startTime': datetime.datetime.strftime(start_obj, "%I:%M %p"),
        'duration': str(end_obj - start_obj).split('.')[0]
    }
    return json.dumps(result)


@app.route('/users/<user_id>/sweeps/<sweep_id>/snapshots')
@cross_origin()
def get_sweep_snapshots(user_id, sweep_id):
    '''Return a list of the snapshots of `user_id`'s sweep, `sweep_id`, sorted from the earliest to the latest, at `/users/<user_id>/sweeps/<sweep_id>/snapshots`.'''
    sweep = db.find_one('sweeps', {'_id': sweep_id})
    collection = db.find('snapshots', {
        '$and': [{'datetime': {'$gte': sweep['sweepStart']}},
                 {'datetime': {'$lte': sweep['sweepEnd']}}]}
                 ).sort('datetime')
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
    '''Return the user `user_id` at `/users/<user_id>`.'''
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
        'gender': gender[user['gender']]
    }
    return json.dumps(u)


@app.route('/users/<user_id>/snapshots')
@cross_origin()
def get_user_snapshots(user_id):
    '''Return a list of `user_id`'s snapshots at `/users/<user_id>/snapshots`.'''
    collection = db.find('snapshots',
                         {'userId': int(user_id)},
                         {'_id': 1, 'datetime': 1}).sort('datetime')
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
    '''Return the snapshot `snapshot_id` of the user `user_id` at `/users/<user_id>/snapshots/<snapshot_id>`.'''
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
    '''Return the result `result_name` of `user_id`'s snapshot, `snapshot_id`, at `/users/<user_id>/snapshots/<snapshot_id>/<result_name>`.'''
    snapshot = db.find_one('snapshots', {'_id': snapshot_id})
    name = auxiliary.snake_to_lower_camel(result_name, '-')
    if name in snapshot['results']:
        result = snapshot['results'][name]
        if name in ['colorImage', 'depthImage']:
            result['data'] = f"/users/{user_id}/snapshots/{snapshot_id}/{result_name}/data"
            del result['path']
        return json.dumps(result)


@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>/data')
@cross_origin()
def get_result_data(user_id, snapshot_id, result_name):
    '''Return images (either color images or depth images) that are saved to disk, at `/users/<user_id>/snapshots/<snapshot_id>/<result_name>/data`.'''
    snapshot = db.find_one('snapshots', {'_id': snapshot_id})
    name = auxiliary.snake_to_lower_camel(result_name, '-')
    if name in snapshot['results']:
        if name in ['colorImage', 'depthImage']:
            return send_file(
                snapshot['results'][name]['path'], mimetype='image/gif')


def run_api_server(database_url,
                   host='127.0.0.1',
                   port=5000):
    '''Listen on `host`:`port` and serve data from `database_url`.'''
    global db
    db = Database(database_url)
    app.run(host=host, port=port)


@main.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=5000)
@click.option('-d', '--database', default=None)
def run_server(host, port, database):
    run_api_server(database, host, port)


if __name__ == '__main__':
    main()
