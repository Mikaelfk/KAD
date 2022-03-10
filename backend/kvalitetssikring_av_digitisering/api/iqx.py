from flask import Blueprint, request
from flask.wrappers import Response
import json

from ..tools.iq_analyzer_x.iqx import run_analysis

iqx_endpoint = Blueprint("iqx_endpoint", __name__)


@iqx_endpoint.route("/api/analyze/device/iqx", methods=["POST"])
def analyze():
    target = request.args.get("target")

    # make sure it's a valid target
    match target:
        case "UTT":
            print("uwu")

        case None | "":
            return Response(json.dumps({"error:": "no target specified"}), status=400)

        case _:
            return Response(json.dumps({"error": "invalid target"}), status=400)

    return Response(status=200)
