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
