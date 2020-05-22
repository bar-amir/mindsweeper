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
            pika.ConnectionParameters(host=url.hostname, port=url.port))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='ms_exchange',
                                      exchange_type='topic')


    def publish(self, msg):
        topic = f"{msg['type']}.{msg['status']}"
        self.channel.basic_publish(exchange='ms_exchange',
                                   routing_key=topic,
                                   body=bson.encode(msg))
        click.echo(f" [x] Published {topic}")
        #self.connection.close()


    def start_parser(self, function, msg_types):
        def callback(ch, method, properties, body):
            click.echo(' [x] Received message')
            self.publish(function(bson.decode(body)))

        parser_name = function.__name__
        self.channel.queue_declare(queue=parser_name)
        click.echo(' [*] Waiting for messages. To exit press CTRL+C')
        for t in msg_types:
            self.channel.queue_bind(exchange='ms_exchange',
                                    queue=parser_name,
                                    routing_key=f'{t}.unparsed')
        self.channel.basic_consume(queue=parser_name,
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()

    def start_saver(self, function):
        def callback(ch, method, properties, body):
            click.echo(' [x] Received message')
            function(bson.decode(body))

        self.channel.queue_declare(queue='saver')
        self.channel.queue_bind(exchange='ms_exchange',
                                queue='saver',
                                routing_key='*.ready')
        click.echo(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.basic_consume(queue='ms_queue',
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()
