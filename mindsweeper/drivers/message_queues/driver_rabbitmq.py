import bson
import click
import pika
from urllib.parse import urlparse
from ...utils import aux, config
import time


class RabbitMQ:
    def __init__(self, url):
        self.url = urlparse(url)
        self.connect()

    def connect(self):
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
