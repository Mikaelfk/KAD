"""Module for OS QM-Tool endpoint.

This module is for use with Flask, and the methods should therefore never be called directly.
It defines endpoints for performing analysis with OS QM-Tool.
"""
import json
import multiprocessing.pool as ThreadPool

from flask import Blueprint, request
from flask.wrappers import Response

from kvalitetssikring_av_digitisering.config import Config
from kvalitetssikring_av_digitisering.tools.os_qm_tool.oqt import (
    run_analyses_all_images,
)
from kvalitetssikring_av_digitisering.utils.path_helpers import get_session_image_file
from kvalitetssikring_av_digitisering.utils.session_manager import (
    create_analysis_folders,
    create_session,
)
from kvalitetssikring_av_digitisering.utils.file_helpers import is_file_empty

oqt_endpoint = Blueprint("oqt_endpoint", __name__)


# Create pool of n threads
pool = ThreadPool.ThreadPool(
    int(Config.config().get(section="OS QM-Tool", option="ConcurrentSessions"))
)


@oqt_endpoint.route("/api/analyze/device/oqt", methods=["POST"])
def analyze():
    """An endpoint which initializes a session and starts analysis on all images uploaded

    Returns:
        str: a json response with the session id if request is valid, an error otherwise
    """
    target = request.args.get("target")

    match target:
        case "UTT" | "TE263" | "GTObject" | "GTDevice":
            print("Target which is used: " + target)
            files = request.files.getlist("files")
            session_id = create_session()

            for file in files:
                if not is_file_empty(file):
                    file.save(get_session_image_file(session_id, str(file.filename)))

            create_analysis_folders(session_id)

            pool.apply_async(
                run_analyses_all_images,
                args=(session_id, target),
            )

            return Response(json.dumps({"session_id": str(session_id)}), status=200)

        case None | "":
            return Response(json.dumps({"error": "no target specified"}), status=400)

        case _:
            return Response(json.dumps({"error": "invalid target"}), status=400)
