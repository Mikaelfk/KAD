"""Simple main class for running.

"""
from flask import Flask

from .api import validate_endpoint


def start():
    """Starts listening for connections

    This method initializes the flask app, registers endpoints and starts the listening.
    """

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1GB

    app.register_blueprint(validate_endpoint)

    app.run(host="0.0.0.0")
