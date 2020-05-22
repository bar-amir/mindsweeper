from .utils import drivers
import pika
import pymongo
import click

def saver_factory(function, database_url):
    def saver(msg):
        return function(msg, database_url)
    return saver

def saver(msg, database_url=None):
    db = drivers.Database(database_url)
    db.save_msg(msg)

@click.group()
def main():
    pass

@main.command()
@click.argument('database_url', nargs=1)
@click.argument('message_queue_url', nargs=1)
def run_saver(database_url=None, message_queue_url=None):
    mq = drivers.MessageQueue(message_queue_url)
    mq.start_saver(saver_factory(saver, database_url))

@main.command()
@click.option('-d', '--database', nargs=1, default=None)
@click.argument('topic_name', nargs=1)
@click.argument('data', nargs=1)
def save(topic_name, data, database=None):
    saver(data, database)

if __name__ == '__main__':
    main()
    