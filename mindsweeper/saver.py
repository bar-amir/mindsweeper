import drivers as d

class Saver:
    def __init__(self, message_queue_url=None, database_url=None):
        # Connect to message queue
        mq = d.MessageQueue(message_queue_url)

        # Connect to database
        db = d.Database(database_url)

    def save(topic_name, data):
        
        pass