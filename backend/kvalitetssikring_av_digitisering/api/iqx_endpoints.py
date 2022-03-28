"""Module for IQ Analyzer X endpoint.

This module is for use with Flask, and the methods should therefore never be called directly.
It defines endpoints for performing analysis with IQ Analyzer X.
"""

import json
import multiprocessing.pool as ThreadPool

from flask import Blueprint, request
from flask.wrappers import Response
from kvalitetssikring_av_digitisering.config import Config
from kvalitetssikring_av_digitisering.tools.iq_analyzer_x.iqx import (
    run_before_after_target_analysis,
)
from kvalitetssikring_av_digitisering.utils.path_helpers import get_session_image_file
from kvalitetssikring_av_digitisering.utils.session_manager import (
    create_analysis_folders,
    create_session,
)
from kvalitetssikring_av_digitisering.utils.file_helpers import is_file_empty

iqx_endpoint = Blueprint("iqx_endpoint", __name__)

# Create pool of n threads
pool = ThreadPool.ThreadPool(
    int(Config.config().get(section="IQ ANALYZER X", option="ConcurrentSessions"))
)


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
            files = request.files.getlist("files")

            if is_file_empty(before_target) or is_file_empty(after_target):
                return Response(
                    json.dumps(
                        {"error": "before_target or after_target not specified"},
                    ),
                    status=400,
                )

            before_target_path = get_session_image_file(
                session_id, str(before_target.filename)
            )

            after_target_path = get_session_image_file(
                session_id, str(after_target.filename)
            )

            before_target.save(before_target_path)
            after_target.save(after_target_path)

            create_analysis_folders(session_id)

            for file in files:
                if not is_file_empty(file):
                    file.save(get_session_image_file(session_id, str(file.filename)))

            pool.apply_async(
                run_before_after_target_analysis,
                args=(before_target.filename, after_target.filename, session_id),
            )

            return Response(json.dumps({"session_id": str(session_id)}), status=200)

        case None | "":
            return Response(json.dumps({"error": "no target specified"}), status=400)

        case _:
            return Response(json.dumps({"error": "invalid target"}), status=400)
