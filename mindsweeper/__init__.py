from .server import run_server
from .client import upload_thought
from .web import run_webserver
from .thought import Thought

from flask import Flask

app = Flask(__name__)

from mindsweeper import routes
