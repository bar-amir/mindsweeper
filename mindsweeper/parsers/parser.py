import pika

class Parser:
    def __init__(self, parser_func):
        self.parser_func = parser_func
    
    def __call__(self):
        self.start()

    def parse(self, body):
        msg = self.parser_func(body)
        self.send(msg)

    def send(self, msg):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='mindsweeper', exchange_type='direct')
        channel.basic_publish(exchange='mindsweeper', routing_key='saver', body=msg)
        print(f' [x] Sent {msg}')

    def start(self):
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='mindsweeper', exchange_type='direct')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='parsers',
                       queue=queue_name,
                       routing_key=self.parser_func.__name__)

        def callback(ch, method, properties, body):
            print(f' [x] Received {body}')
            self.parse(body)

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()