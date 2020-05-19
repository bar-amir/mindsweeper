from .utils import drivers as d
import pika

class Saver:
    def __init__(self, message_queue_url=None, database_url=None):
        # Connect to message queue
        mq = d.MessageQueue(message_queue_url)

        # Connect to database
        db = d.Database(database_url)

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

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def save(topic_name, data):
        pass

if __name__ == '__main__':
    s = Saver()
    s.start()