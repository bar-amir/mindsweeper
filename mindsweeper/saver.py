from .drivers import MessageQueue, Database
import click


class Saver:
    def __init__(self, database_url):
        self.db = Database(database_url)
    
    def save(self, msg):
        self.db.upsert(msg)


@click.group()
def main():
    pass


@main.command()
@click.argument('database_url', nargs=1)
@click.argument('message_queue_url', nargs=1)
def run_saver(database_url=None, message_queue_url=None):
    mq = MessageQueue(message_queue_url)
    mq.start_saver(Saver(database_url))


@main.command()
@click.option('-d', '--database', nargs=1, default=None)
@click.argument('topic_name', nargs=1)
@click.argument('data', nargs=1)
def save(topic_name, data, database=None):
    db = Database(database)
    db.upsert(data)


if __name__ == '__main__':
    main()
