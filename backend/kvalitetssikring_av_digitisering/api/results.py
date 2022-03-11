from flask import Blueprint, request
from flask.wrappers import Response
import json


results_endpoint = Blueprint("results_endpoint", __name__)

@results_endpoint.route("/api/results/<session_id>", methods=["GET"])
def results(session_id):
    print(session_id)
    return Response(json.dumps({"session_id": session_id}), status=200)
