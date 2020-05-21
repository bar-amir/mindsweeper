import pika
import json
import bson
from . import aux

class Database:
    drivers = {}

    def __init__(self, database_url):
        if not database_url:
            database_url = aux.DEFAULT_DATABASE

class MessageQueue:
    drivers = {}

    def __init__(self, message_queue_url):
        if not message_queue_url:
            message_queue_url = aux.DEFAULT_MESSAGE_QUEUE
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='mindsweeper', exchange_type='topic')
        for p in aux.get_parsers_list():
            self.channel.queue_declare(queue=p)
            self.channel.queue_bind(exchange='mindsweeper',
                        queue=p,
                        routing_key=f'{p}.unparsed')
        print(' [*] Waiting for messages. To exit press CTRL+C')

    def publish(self, msg):
        msg_type = aux.camel_to_snake(msg['type'])
        self.channel.basic_publish(exchange='mindsweeper',
                                   routing_key=f"{msg_type}.{msg['status']}",
                                   body=bson.encode(msg))
        print(f" [x] Published {msg_type}.{msg['status']}")

    def start_parser(self, function):
        def callback(ch, method, properties, body):
            print(f" [x] Received raw message")
            self.publish(function(bson.decode(body)))

        self.channel.basic_consume(queue=function.__name__, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()