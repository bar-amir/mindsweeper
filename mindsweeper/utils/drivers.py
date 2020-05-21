import pika
import json
import bson
from . import aux

class Database:
    drivers = {}

    def __init__(self, database_url):
        if not database_url:
            database_url = 'postgresql://127.0.0.1:5432/'

class MessageQueue:
    drivers = {}

    def __init__(self, message_queue_url):
        if not message_queue_url:
            message_queue_url = 'rabbitmq://127.0.0.1:5672/'
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='mindsweeper', exchange_type='topic')
        print(' [*] Waiting for messages. To exit press CTRL+C')

    def publish(self, msg):
        msg_type = aux.camel_to_snake(msg['type'])
        self.channel.basic_publish(exchange='mindsweeper',
                                   routing_key=f"{msg_type}.{msg['status']}",
                                   body=bson.encode(msg))
        print(f" [x] Published {msg_type}.{msg['status']}")

    def close(self):
        self.connection.close()