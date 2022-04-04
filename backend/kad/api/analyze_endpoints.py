"""Module for analyzing images with IQE software

This module is for use with Flask, and the methods should therefore never be called directly.
"""
import json
import logging
import multiprocessing.pool as ThreadPool
from typing import Dict, List

from flask import Blueprint, request
from flask.wrappers import Response
from kad.config import Config
from kad.tools.analysis_run import run_device_analysis, run_object_analysis
from kad.utils.file_helpers import are_files_valid, is_file_empty
from kad.utils.filename_handler import save_uploaded_files
from kad.utils.session_manager import create_analysis_folders, create_session
from werkzeug.datastructures import FileStorage

analyze_endpoint = Blueprint("analyze_endpoint", __name__)

# Create pool of n threads for how many analyses can run at once
pool = ThreadPool.ThreadPool(
    int(Config.config().get(section="IQ ANALYZER X", option="ConcurrentSessions"))
)


@analyze_endpoint.route("/api/analyze/device", methods=["POST"])
def analyze_device():
    """An endpoint for creating a session and starting analysis on device level.

    Returns:
        Response: a JSON response which contains the session id.
    """

    # for easy checking before start
    supported_iqes = ["IQX", "OQT"]
    supported_targets = {
        "IQX": ["UTT"],
        "OQT": ["UTT", "GTDevice"],
    }

    ## First check request args

    # get request args
    iqes = request.args.get("iqes")
    target = request.args.get("target")

    # fail fast time!
    error_response = check_iqes_and_targets(
        iqes,
        target,
        supported_iqes,
        supported_targets,
    )
    if error_response is not None:
        return error_response

    ## Then check files

    # check if fields are there in request
    if not "before_target" in request.files:
        return Response(
            json.dumps({"error": "before_target not specified"}),
            status=400,
        )
    if not "after_target" in request.files:
        return Response(
            json.dumps({"error": "after_target not specified"}),
            status=400,
        )

    # get files :D
    before_target = request.files["before_target"]
    after_target = request.files["after_target"]
    files = request.files.getlist("files")

    # create list of all files
    all_files = files
    all_files.append(before_target)
    all_files.append(after_target)
    file_names = []

    # checkem
    error_response = check_files([before_target, after_target], all_files)
    if error_response is not None:
        return error_response

    # at this point we prob good lets start session
    logging.getLogger().info(
        "Got request to start session with %s and target %s", iqes, target
    )
    session_id = create_session()

    # save files
    before_target_filename = save_uploaded_files(
        session_id, [before_target], file_names
    )
    after_target_filename = save_uploaded_files(session_id, [after_target], file_names)

    # save rest of uploaded files if there are any
    save_uploaded_files(session_id, files, file_names)

    # create analysis folders for targets
    create_analysis_folders(session_id)

    ## Now it's runny time

    pool.apply_async(
        run_device_analysis,
        args=(before_target_filename, after_target_filename, session_id, iqes, target),
    )

    return Response(json.dumps({"session_id": str(session_id)}), status=200)


@analyze_endpoint.route("/api/analyze/object", methods=["POST"])
def analyze_object():
    """An endpoint for creating a session and starting analysis on object level.

    Returns:
        Response: a JSON response which contains the session id.
    """

    # for easy checking before start
    supported_iqes = ["OQT"]
    supported_targets = {
        "OQT": ["TE263", "GTObject"],
    }

    ## First check request args

    # get request args
    iqes = request.args.get("iqes")
    target = request.args.get("target")

    # fail fast time!
    error_response = check_iqes_and_targets(
        iqes,
        target,
        supported_iqes,
        supported_targets,
    )
    if error_response is not None:
        return error_response

    ## Then check files

    files = request.files.getlist("files")
    if len(files) == 0:
        return Response(json.dumps({"error": "no files uploaded"}), status=400)

    # checkem
    error_response = check_files([], files)
    if error_response is not None:
        return error_response

    ## we good lets do the session stuff

    session_id = create_session()
    save_uploaded_files(session_id, files)
    create_analysis_folders(session_id)

    ## Now it's runny time

    pool.apply_async(
        run_object_analysis,
        args=(session_id, iqes, target),
    )

    return Response(json.dumps({"session_id": str(session_id)}), status=200)


##########################
# NON-ENDPOINT FUNCTIONS #
##########################


def check_iqes_and_targets(
    iqes: str | None,
    target: str | None,
    supported_iqes: List[str],
    supported_targets: Dict[str, List[str]],
):
    """Checks if iqes and/or target is supported with referance data

    Helper function for endpoints.

    Returns:
        Response | None: a JSON response which contains the appropriate error, or none if good
    """

    # iqe arg is empty
    if iqes is None or not iqes:
        return Response(json.dumps({"error": "no iqes specified"}), status=400)

    # target arg is empty
    if target is None or not target:
        return Response(json.dumps({"error": "no target specified"}), status=400)

    # iqe is not supported
    if iqes not in supported_iqes:
        return Response(json.dumps({"error": f"{iqes} not supported"}), status=400)

    # iqe does not support target
    if target not in supported_targets[iqes]:
        return Response(
            json.dumps({"error": f"{iqes} does not support target {target}"}),
            status=400,
        )

    return None


def check_files(
    empty_file_check: List[FileStorage],
    filetype_check: List[FileStorage],
):
    """Checks if uploaded files are good.

    Helper function for endpoints.

    Args:
        empty_file_check: List of files to check if FileStorage actually contains data
        filetype_check: List of files to check if file is of correct type (TIFF, JPEG)

    Returns
        Response | None: a JSON response which contains the appropriate error, or none if good
    """

    # check if targets exist
    for file in empty_file_check:
        if is_file_empty(file):
            return Response(
                json.dumps(
                    {"error": "missing file(s). Check request"},
                ),
                status=400,
            )

    # check if files are valid images
    files_valid, file_name = are_files_valid(filetype_check)
    if not files_valid:
        return Response(
            json.dumps(
                {"error": f"File extension not supported for file {str(file_name)}"},
            ),
            status=400,
        )

    return None
