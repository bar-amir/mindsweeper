from .utils import drivers
import pika
import pymongo
import click

class Saver:
    def __init__(self, message_queue_url=None, database_url=None):
        # Connect to database
        #db = d.Database(database_url)
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['mindsweeper']
        
        # Connect to message queue
        mq = drivers.MessageQueue(message_queue_url)
        mq.start_saver(self._save)

    def _save(self, msg):
        db = self.db
        data = msg['data']
        # Check user ID to see if it exists
        if msg['type'] == 'user':
            if db['users'].count_documents({'_id': msg['data']['userId']}) == 0:
                print(' [*] Creating new user')
                user = {
                    '_id' : data['userId'],
                    'username': data['username'],
                    'birthday': data['birthday'],
                    'gender': data['gender'],
                    'snapshots': []
                }
                db['users'].insert_one(user)
                print(f" [X] Created user {msg['data']['userId']}")
            else:
                print(f" [*] User {msg['data']['userId']} already exists")
        else:
            print(f" [*] Adding {msg['type']}")
            if db['snapshots'].count_documents({'_id': f"{msg['userId']}-{msg['datetime']}"}) == 0:
                #print(f' [*] Snapshot for this message does not exist. adding...')
                snapshot = {
                    '_id': f"{msg['userId']}-{msg['datetime']}",
                    'userId': msg['userId'],
                    'datetime': msg['datetime'],
                }
                db['snapshots'].insert_one(snapshot)
                #print(' [X] Added new snapshot.')
                user_query = {'_id': msg['userId']}
                new_values = { '$push': { 'snapshots': f"{msg['userId']}-{msg['datetime']}" } }
                db['users'].update_one(user_query, new_values)
                #print(' [X] Updated user snapshot list.')
            snapshot_query = {'_id': f"{msg['userId']}-{msg['datetime']}"}
            new_values = {'$set': {f"results.{msg['type']}": data}}
            print(db['snapshots'].find_one(snapshot_query))
            db['snapshots'].update_one(snapshot_query, new_values)
            #print(f" [X] Added {msg['type']} to snapshot {msg['userId']}-{msg['datetime']}")

@click.group()
def main():
    pass

@main.command()
@click.argument('database_url', nargs=1)
@click.argument('message_queue_url', nargs=1)
def run_saver(database_url, message_queue_url):
    saver = Saver(message_queue_url, database_url)

@main.command()
@click.option('-d', '--database', nargs=1)
@click.argument('topic_name', nargs=1)
@click.argument('data', nargs=1)
def save(database=None, topic_name, data):
    saver = Saver(database_url=data)
    saver._saver(data)

if __name__ == '__main__':
    main()
    