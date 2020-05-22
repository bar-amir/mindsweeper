import pika
import bson
from . import aux
import pymongo
from .. import config


class Database:
    drivers = {}

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
                user = {
                    '_id': msg['userId'],
                    'datetime': msg['datetime'],
                    'username': data['username'],
                    'birthday': data['birthday'],
                    'gender': data['gender'],
                }
                db['users'].insert_one(user)
                # print(f" [X] Created user {msg['userId']}")
            else:
                pass
                # print(f" [*] User {msg['userId']} already exists")
        elif msg['type'] == 'sweep_summary':
            if db['users'].count_documents({'sweepStart': data['sweepStart']}) == 0:
                sweep = {
                    '_id': f"{msg['userId']}-{msg['datetime']}-{data['numOfSnapshots']}",
                    'userId': msg['userId'],
                    'datetime': msg['datetime'],
                    'sweepStart': data['sweepStart'],
                    'sweepEnd': data['sweepEnd'],
                    'numOfSnapshots': data['numOfSnapshots']
                }
                db['sweeps'].insert_one(sweep)
        else:
            # print(f" [*] Adding {msg['type']}")
            if db['snapshots'].count_documents({'_id': f"{msg['userId']}-{msg['datetime']}"}) == 0:
                # print(f' [*] Snapshot for this message does not exist. adding...')
                snapshot = {
                    '_id': f"{msg['userId']}-{msg['datetime']}",
                    'userId': msg['userId'],
                    'datetime': msg['datetime'],
                }
                db['snapshots'].insert_one(snapshot)
                # print(' [X] Added new snapshot.')

                # print(' [X] Updated user snapshot list.')
            snapshot_query = {'_id': f"{msg['userId']}-{msg['datetime']}"}
            new_values = {'$set': {f"results.{msg['type']}": data}}
            # print(db['snapshots'].find_one(snapshot_query))
            db['snapshots'].update_one(snapshot_query, new_values)
            # print(f" [X] Added {msg['type']} to snapshot {msg['userId']}-{msg['datetime']}")

class MessageQueue:
    drivers = {}

    def __init__(self, message_queue_url):
        if not message_queue_url:
            message_queue_url = config.DEFAULT_MESSAGE_QUEUE
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='mindsweeper', exchange_type='topic')
        for p in aux.get_parsers_list():
            self.channel.queue_declare(queue=p)
            self.channel.queue_bind(exchange='mindsweeper',
                                    queue=p,
                                    routing_key=f'{p}.unparsed')
        self.channel.queue_declare(queue='saver')
        self.channel.queue_bind(exchange='mindsweeper',
                                queue='saver',
                                routing_key=f'*.parsed')
        self.channel.queue_bind(exchange='mindsweeper',
                                queue='saver',
                                routing_key=f'*.uploaded')
        print(' [*] Waiting for messages. To exit press CTRL+C')

    def publish(self, msg):
        msg_type = aux.camel_to_snake(msg['type'])
        self.channel.basic_publish(exchange='mindsweeper',
                                   routing_key=f"{msg_type}.{msg['status']}",
                                   body=bson.encode(msg))
        print(f" [x] Published {msg_type}.{msg['status']}")

    def start_parser(self, function):
        def callback(ch, method, properties, body):
            #print(f" [x] Received message")
            self.publish(function(bson.decode(body)))
        self.channel.basic_consume(queue=function.__name__, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def start_saver(self, function):
        def callback(ch, method, properties, body):
            #print(f" [x] Received message")
            function(bson.decode(body))
        self.channel.basic_consume(queue='saver', on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
