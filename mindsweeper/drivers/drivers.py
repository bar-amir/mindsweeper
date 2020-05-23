import pika
import bson
from . import aux
import pymongo
from .. import config


class Database:
    def __init__(self, database_url):
        if not database_url:
            database_url = config.DEFAULT_DATABASE
        self.client = pymongo.MongoClient(database_url)
        self.db = self.client['mindsweeper']

    def save_msg(self, msg):
        db = self.db
        data = msg['data']
        # Check user ID to see if it exists
        if msg['type'] == 'user':
            if db['users'].count_documents({'_id': msg['userId']}) == 0:
                # print(' [*] Creating new user')
                
                # print(f" [X] Created user {msg['userId']}")
            else:
                pass
                # print(f" [*] User {msg['userId']} already exists")
        elif msg['type'] == 'sweep_summary':
            if db['users'].count_documents({'sweepStart': data['sweepStart']}) == 0:
                
        else:
            # print(f" [*] Adding {msg['type']}")
            if db['snapshots'].count_documents({'_id': f"{msg['userId']}-{msg['datetime']}"}) == 0:
                # print(f' [*] Snapshot for this message does not exist. adding...')
                
                # print(' [X] Added new snapshot.')

                # print(' [X] Updated user snapshot list.')
            snapshot_query = {'_id': f"{msg['userId']}-{msg['datetime']}"}
            new_values = {'$set': {f"results.{msg['type']}": data}}
            # print(db['snapshots'].find_one(snapshot_query))
            db['snapshots'].update_one(snapshot_query, new_values)
            # print(f" [X] Added {msg['type']} to snapshot {msg['userId']}-{msg['datetime']}")
