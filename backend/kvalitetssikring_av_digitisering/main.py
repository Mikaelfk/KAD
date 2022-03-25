"""Simple main class for running.

"""
import os

from flask import Flask
from flask_cors import CORS

from kvalitetssikring_av_digitisering.api import (
    iqx_endpoint,
    oqt_endpoint,
    results_endpoint,
    session_endpoint,
    validate_endpoint,
    download_endpoint,
)
from kvalitetssikring_av_digitisering.config import Config


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
    app.register_blueprint(oqt_endpoint)
    app.register_blueprint(download_endpoint)

    # Create storage folder
    os.makedirs(
        Config.config().get(section="API", option="StorageFolder"), exist_ok=True
    )

    app.run(host="0.0.0.0", port=int(Config.config().get(section="API", option="Port")))
