"""Module for results endpoint.

This module is for use with Flask, and the methods should therefore never be called directly.
It defines endpoints for getting the results of a session.
"""

import json
import os

from flask import Blueprint
from flask.wrappers import Response

from ..config import Config
from ..session_manager import check_session_exists

results_endpoint = Blueprint("results_endpoint", __name__)


@results_endpoint.route("/api/results/<session_id>", methods=["GET"])
def results(session_id):
    """Method for retrieving the overall results of a session.

    Returns:
        A HTTP Response with corresponding status code and data
    """

    session_results_file = os.path.join(
        Config.config().get(section="API", option="StorageFolder"),
        session_id,
        "results.json",
    )

    if check_session_exists(session_id):
        return Response(json.dumps({"error": "session does not exist"}), status=400)

    with open(session_results_file, "a+", encoding="UTF-8") as json_file:
        json_file.seek(0)

        if os.path.getsize(session_results_file) > 0:
            # this doesn't seem great, but works, so maybe fix in future?
            return Response(json.dumps(json.load(json_file)), status=200)

        return Response(json.dumps({"error": "no results"}), status=404)
