"""Simple main class for running.

"""
from flask import Flask
from flask_cors import CORS
from .config import Config

from .api import validate_endpoint
from .api import session_endpoint
from .api import iqx_endpoint
from .api import results_endpoint


def start():
    """Starts listening for connections

    This method initializes the flask app, registers endpoints and starts the listening.
    """

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1GB
    # Compliant
    CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "False"}})

    app.register_blueprint(validate_endpoint)
    app.register_blueprint(session_endpoint)
    app.register_blueprint(iqx_endpoint)
    app.register_blueprint(results_endpoint)

    app.run(host="0.0.0.0", port=int(
        Config.config().get(section="API", option="Port")))
