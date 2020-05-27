'''Savers consume messages with 'ready' status from a message queue and save them to a database.'''

import bson
import click
from .drivers import Database
from .drivers import MessageQueue


class Saver:
    def __init__(self, database_url):
        self.db = Database(database_url)

    def save(self, topic, msg):
        '''Save a message to the Saver's database. The specification of the project requires receiving the message queue's relevant topic name, however, in this implementation, the topic is a combination of the message type and its status, so this function ignores `topic`.'''
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
@click.option('-p', '--path', is_flag=True, nargs=1, default=None)
@click.argument('topic_name', nargs=1)
@click.argument('data', nargs=1)
def save(topic_name, data, path, database=None):
    '''Save the message `data` to `database`. If the flag `--path` is set, `data` would be regarded as a path to a file containing the message. The message should be encoded with BSON, same as if it was consumed from the message queue. This implementation ignores the value of `topic_name`.'''
    if path:
        f = open(data, 'rb')
        data = bson.decode(f.read())
        f.close()
    db = Database(database)
    db.upsert(data)


if __name__ == '__main__':
    main()
