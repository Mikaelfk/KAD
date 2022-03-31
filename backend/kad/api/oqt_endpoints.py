"""Module for OS QM-Tool endpoint.

This module is for use with Flask, and the methods should therefore never be called directly.
It defines endpoints for performing analysis with OS QM-Tool.
"""
import json
import multiprocessing.pool as ThreadPool

from flask import Blueprint, request
from flask.wrappers import Response

from kad.config import Config
from kad.tools.os_qm_tool.oqt import (
    run_analyses_all_images,
)
from kad.utils.session_manager import (
    create_analysis_folders,
    create_session,
)
from kad.utils.filename_handler import save_uploaded_files

oqt_endpoint = Blueprint("oqt_endpoint", __name__)


# Create pool of n threads
pool = ThreadPool.ThreadPool(
    int(Config.config().get(section="OS QM-Tool", option="ConcurrentSessions"))
)


@oqt_endpoint.route("/api/analyze/oqt", methods=["POST"])
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

            if len(files) == 0:
                return Response(json.dumps({"error": "no files uploaded"}), status=400)

            save_uploaded_files(session_id, files)
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
