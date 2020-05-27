'''This file contains values that are used across the app, such as the project's root path, and the default database and message queue settings.'''

from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_MESSAGE_QUEUE = 'rabbitmq://127.0.0.1:5672/'
DEFAULT_DATABASE = 'mongodb://localhost:27017/'
