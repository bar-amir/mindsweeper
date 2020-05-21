import pika
import bson

class Parser:
    def __init__(self, parser_func):
        self.parser_func = parser_func
        self.name = self.parser_func.__name__
    
    def __call__(self):
        self.start()

    def parse(self, body):
        msg = self.parser_func(bson.decode(body))
        self.send(msg)

    def send(self, msg):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='mindsweeper', exchange_type='topic')
        channel.basic_publish(exchange='mindsweeper', routing_key=f'{self.name}.parsed', body=bson.encode(msg))
        print(f' [x] Sent parsed message')

    def start(self):
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='mindsweeper', exchange_type='topic')
        result = channel.queue_declare(queue=self.name)
        channel.queue_bind(exchange='mindsweeper',
                       queue=self.name,
                       routing_key=f'{self.name}.unparsed')

        def callback(ch, method, properties, body):
            print(f" [x] Received raw message")
            self.parse(body)

        channel.basic_consume(
            queue=self.name, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()