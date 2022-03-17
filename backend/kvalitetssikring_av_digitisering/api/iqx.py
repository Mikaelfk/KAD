"""Module for IQ Analyzer X endpoint.

This module is for use with Flask, and the methods should therefore never be called directly.
It defines endpoints for performing analysis with IQ Analyzer X.
"""

import json
import os
import multiprocessing.pool as ThreadPool

from flask import Blueprint, request
from flask.wrappers import Response

from ..config import Config
from ..session_manager import create_analysis_folders, create_session
from ..tools.iq_analyzer_x.iqx import run_analyses

iqx_endpoint = Blueprint("iqx_endpoint", __name__)

# Create pool of n threads
pool = ThreadPool.ThreadPool(int(Config.config().get(
    section="IQ ANALYZER X", option="ConcurrentSessions")))


@iqx_endpoint.route("/api/analyze/device/iqx", methods=["POST"])
def analyze():
    """An endpoint whitch initalizes a session and start analysis on uploaded targets

    Returns:
        Response: a JSON response which contains the session id.
    """
    target = request.args.get("target")

    # make sure it's a valid target
    match target:
        case "UTT":
            print("Target which is used: UTT")
            session_id = create_session()
            before_target = request.files["before_target"]
            after_target = request.files["after_target"]

            # TODO: also get the rest of the images from request.files["files"] so metadata can be added to them.

            before_target_path = os.path.join(
                Config.config().get(section="API", option="StorageFolder"),
                session_id,
                "images",
                before_target.filename,
            )
            after_target_path = os.path.join(
                Config.config().get(section="API", option="StorageFolder"),
                session_id,
                "images",
                after_target.filename,
            )

            before_target.save(before_target_path)
            after_target.save(after_target_path)

            create_analysis_folders(session_id)

            pool.apply_async(run_analyses, args=(
                before_target.filename, after_target.filename, session_id))

            return Response(json.dumps({"session_id": str(session_id)}), status=200)

        case None | "":
            return Response(json.dumps({"error:": "no target specified"}), status=400)

        case _:
            return Response(json.dumps({"error": "invalid target"}), status=400)
