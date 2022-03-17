"""Module for session endpoint.

This module is for use with Flask, and the methods should therefore never be called directly.
It defines endpoints for managing sessions.
"""

import json

from flask import Blueprint, request
from flask.wrappers import Response
from kvalitetssikring_av_digitisering.utils.session_manager import (
    check_session_exists,
    create_analysis_folders,
    create_session,
    update_session_status,
)

# const
HTTP_INVALID_JSON = "invalid json"


session_endpoint = Blueprint("session_endpoint", __name__)


@session_endpoint.route("/api/session/create", methods=["GET"])
def create():
    """Method for creating a session.

    Returns:
        A HTTP Response with corresponding status code and data
    """
    session_id = create_session()

    return Response(json.dumps({"session_id": session_id}), status=200)


@session_endpoint.route("/api/session/updateStatus", methods=["PATCH"])
def update():
    """Method for updating the status of a session.

    Returns:
        A HTTP Response with corresponding status code and data
    """
    if request.is_json:
        data = request.get_json()
        if data is not None:
            session_id = data.get("session_id")
            new_status = data.get("status")
        else:
            return Response(json.dumps({"error": HTTP_INVALID_JSON}), status=400)

        if not check_session_exists(session_id):
            return Response(json.dumps({"error": "session does not exist"}), status=400)

        update_session_status(session_id, new_status)
        return Response(status=200)

    return Response(json.dumps({"error": HTTP_INVALID_JSON}), status=400)


@session_endpoint.route("/api/session/createAnalysisFolders", methods=["GET"])
def create_folders():
    """Method for creating analysis folders for a session.

    Returns:
        A HTTP Response with corresponding status code and data
    """
    if request.is_json:
        data = request.get_json()
        if data is not None:
            session_id = data.get("session_id")
        else:
            return Response(json.dumps({"error": HTTP_INVALID_JSON}), status=400)

        if not check_session_exists(session_id):
            return Response(json.dumps({"error": "session does not exist"}), status=400)

        create_analysis_folders(session_id)

        return Response(status=200)

    return Response(json.dumps({"error": HTTP_INVALID_JSON}))


@session_endpoint.route("/api/session/exists", methods=["GET"])
def check_exists():
    """Method checking if a session exists.

    Returns:
        A HTTP Response with corresponding status code and data
    """
    if request.is_json:
        if request.json is not None:
            session_id = request.json.get("session_id")
        else:
            return Response(json.dumps({"error": HTTP_INVALID_JSON}), status=400)

        exists = check_session_exists(session_id)
        return Response(json.dumps({"exists": exists}), status=200)

    return Response(json.dumps({"error": HTTP_INVALID_JSON}))
