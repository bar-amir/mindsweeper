import bson
import click
import pika
from urllib.parse import urlparse
from ...utils import config


class RabbitMQ:
    def __init__(self, url=None):
        if not url:
            url = config.DEFAULT_MESSAGE_QUEUE
        url = urlparse(url)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=url.host, port=url.port))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='ms_exchange',
                                      exchange_type='topic')

    def publish(self, msg):
        self.channel.basic_publish(exchange='mindsweeper',
                                   routing_key=f"{msg['type']}.{msg['status']}",
                                   body=bson.encode(msg))
        click.echo(f" [x] Published {msg['type']}.{msg['status']}")

    def start_parser(self, function, msg_types):
        def callback(ch, method, properties, body):
            click.echo(' [x] Received message')
            self.publish(function(bson.decode(body)))
        click.echo(' [*] Waiting for messages. To exit press CTRL+C')
        for t in msg_types:
            self.channel.queue_bind(exchange='topic_logs',
                                    queue='ms_queue',
                                    routing_key=f'{t}.unparsed')
        self.channel.basic_consume(queue='ms_queue',
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()

    def start_saver(self, function):
        def callback(ch, method, properties, body):
            click.echo(' [x] Received message')
            function(bson.decode(body))
        self.channel.queue_bind(exchange='topic_logs',
                                queue='ms_queue',
                                routing_key='*.ready')
        click.echo(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.basic_consume(queue='ms_queue',
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
