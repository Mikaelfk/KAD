"""Simple main class for running.

"""
import logging
import os
from datetime import datetime

from flask import Flask
from flask_cors import CORS

from kad.api import (
    analyze_endpoint,
    download_endpoint,
    results_endpoint,
    session_endpoint,
)
from kad.config import Config


def start():
    """Starts listening for connections

    This method initializes the flask app, registers endpoints and starts the listening.
    """

    # Create storage folder
    os.makedirs(
        Config.config().get(section="API", option="StorageFolder"), exist_ok=True
    )

    # Create a dir for logs in cwd
    os.makedirs("kad_logs", exist_ok=True)

    logging.basicConfig(
        filename=f"kad_logs/kad_log-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
        filemode="a",
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1GB
    # Compliant
    CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "False"}})

    app.register_blueprint(results_endpoint)
    app.register_blueprint(download_endpoint)
    app.register_blueprint(session_endpoint)
    app.register_blueprint(analyze_endpoint)

    app.run(host="0.0.0.0", port=int(Config.config().get(section="API", option="Port")))
