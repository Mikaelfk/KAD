from flask import Blueprint, request
from flask.wrappers import Response

import json

from ..session_manager import (
    create_analysis_folders,
    create_session,
    update_session_status,
    check_session_exists,
)

session_endpoint = Blueprint("session_endpoint", __name__)


@session_endpoint.route("/api/session/create", methods=["GET"])
def create():
    session_id = create_session()

    return Response(json.dumps({"session_id": session_id}), status=200)


@session_endpoint.route("/api/session/updateStatus", methods=["PATCH"])
def update():
    if request.is_json:
        data = request.get_json()
        if data is not None:
            session_id = data.get("session_id")
            new_status = data.get("status")
        else:
            return Response(json.dumps({"error": "invalid json"}), status=400)

        if not check_session_exists(session_id):
            return Response(json.dumps({"error": "session does not exist"}), status=400)

        update_session_status(session_id, new_status)
        return Response(status=200)
    else:
        return Response(json.dumps({"error": "invalid json"}), status=400)


@session_endpoint.route("/api/session/createAnalysisFolders", methods=["GET"])
def create_folders():
    if request.is_json:
        data = request.get_json()
        if data is not None:
            session_id = data.get("session_id")
        else:
            return Response(json.dumps({"error": "invalid json"}), status=400)

        if not check_session_exists(session_id):
            return Response(json.dumps({"error": "session does not exist"}), status=400)

        create_analysis_folders(session_id)

        return Response(status=200)


@session_endpoint.route("/api/session/exists", methods=["GET"])
def check_exists():
    if request.is_json:
        if request.json is not None:
            session_id = request.json.get("session_id")
        else:
            return Response(json.dumps({"error": "invalid json"}), status=400)

        exists = check_session_exists(session_id)
        return Response(json.dumps({"exists": exists}), status=200)
