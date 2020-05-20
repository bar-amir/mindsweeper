from .utils import drivers as d
import pika
import pymongo
import json

class Saver:
    def __init__(self, message_queue_url=None, database_url=None):
        # Connect to message queue
        #mq = d.MessageQueue(message_queue_url)
    
        # Connect to database
        #db = d.Database(database_url)
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['mindsweeper']

        self.start()

    def start(self):
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='mindsweeper', exchange_type='direct')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='mindsweeper',
                       queue=queue_name,
                       routing_key='saver')

        def callback(ch, method, properties, body):
            print(f' [x] Received {body}')
            self._save(body)

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def _save(self, data):
        db = self.db
        # Check user ID to see if it exists
        msg = json.loads(data)
        if msg['type'] == 'user':
            if db['users'].count_documents({'_id': msg['data']['userId']}) == 0:
                print(' [*] Creating new user')
                user = {
                    '_id': msg['data']['userId'],
                    'username': msg['data']['username'],
                    'birthday': msg['data']['birthday'],
                    'gender': msg['data']['gender'],
                    'snapshots': []
                }
                db['users'].insert_one(user)
                print(f" [X] Created user {msg['data']['userId']}")
            else:
                print(f" [*] User {msg['data']['userId']} already exists!")
        else:
            print(f" [*] Adding {msg['type']}")
            if db['snapshots'].count_documents({'_id': f"{msg['userId']}-{msg['datetime']}"}) == 0:
                print(f' [*] Snapshot for this message does not exist. adding...')
                snapshot = {
                    '_id': f"{msg['userId']}-{msg['datetime']}",
                    'userId': msg['userId'],
                    'datetime': msg['datetime'],
                }
                db['snapshots'].insert_one(snapshot)
                print(' [X] Added new snapshot.')
                user_query = {'_id': msg['userId']}
                new_values = { '$push': { 'snapshots': msg['datetime'] } }
                db['users'].update_one(user_query, new_values)
                print(' [X] Updated user snapshot list.')
            
            snapshot_query = {'_id': f"{msg['userId']}-{msg['datetime']}"}
            new_values = 
            {'$set': {f"results.{msg['type']}":  msg['data']}}
            db['snapshots'].update_one(snapshot_query, new_values)
            print(f" [X] Added {msg['type']} to snapshot {msg['userId']}-{msg['datetime']}")


    def save(topic_name, data):
        pass

if __name__ == '__main__':
    s = Saver()
    