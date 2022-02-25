import configparser

from flask import Flask
from .api import validate_endpoint
from .config import Config


def start():
    print(Config().config().get(section="API", option="Port"))

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1GB

    app.register_blueprint(validate_endpoint)

    app.run()
