import click
import bson
import pika
import time
from ...utils import aux
from urllib.parse import urlparse


class RabbitMQ:
    def __init__(self, url):
        self.url = urlparse(url)
        self.connect()

    def connect(self):
        '''
        Connect to RabbitMQ, then create the app's exchange and declare
        queues for each parser and for the saver. Bind each queue to their
        topic: Parsers subscribe to messages found in their `msg_types`
        with status 'unparsed'. Saver subscribe to every message with
        status 'ready'.
        '''
        attempts = 0
        while True:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=self.url.hostname,
                        port=self.url.port))
                self.channel = self.connection.channel()
                self.channel.exchange_declare(
                    exchange='ms_exchange',
                    exchange_type='topic')
                for parser_name, msg_types in aux.get_parsers():
                    self.channel.queue_declare(queue=parser_name)
                    for t in msg_types:
                        self.channel.queue_bind(
                            exchange='ms_exchange',
                            queue=parser_name,
                            routing_key=f'{t}.unparsed')
                self.channel.queue_declare(queue='saver')
                self.channel.queue_bind(
                    exchange='ms_exchange',
                    queue='saver',
                    routing_key='*.ready')
                break
            except:
                click.echo('Having trouble connecting to message queue. Trying again in 10 seconds.')
                time.sleep(10)
                attempts += 1

    def publish(self, msg):
        '''Receive a message and publish it to the right topic, according to
        its `type` and `status`.'''
        topic = f"{msg['type']}.{msg['status']}"
        while True:
            try:
                self.channel.basic_publish(
                    exchange='ms_exchange',
                    routing_key=topic,
                    body=bson.encode(msg))
                break
            except:
                click.echo('Having trouble publishing to message queue. Trying to reconnect.')
                self.connect()
        click.echo(f"Published message at {topic}.")
        # self.connection.close()

    def start_parser(self, function, msg_types):
        '''Start a parser as a service.'''
        def callback(ch, method, properties, body):
            click.echo('Received message')
            self.publish(function(bson.decode(body)))
        parser_name = function.__name__
        click.echo('Waiting for messages. (Press CTRL+C to quit)')
        attempts = 0
        while True:
            try:
                self.channel.basic_consume(
                    queue=parser_name,
                    on_message_callback=callback,
                    auto_ack=True)
                self.channel.start_consuming()
            except:
                attempts += 1
                click.echo(f'Having trouble consuming from queue. Trying again in 10 seconds. ({attempts})')
                time.sleep(10)

    def start_saver(self, saver):
        '''Start a saver as a servce by using this connected to
        the message queue.'''
        def callback(ch, method, properties, body):
            click.echo('Received message')
            saver.save(bson.decode(body))
        click.echo('Waiting for messages. (Press CTRL+C to quit)')
        attempts = 0
        while True:
            try:
                self.channel.basic_consume(
                    queue='saver',
                    on_message_callback=callback,
                    auto_ack=True)
                self.channel.start_consuming()
            except:
                attempts += 1
                click.echo(f'Having trouble consuming from queue. Trying again in 10 seconds. ({attempts})')
                time.sleep(10)
