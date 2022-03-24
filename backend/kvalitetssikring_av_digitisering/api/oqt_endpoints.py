from flask import Blueprint, request
from flask.wrappers import Response

from kvalitetssikring_av_digitisering.tools.os_qm_tool.oqt import run_analysis

oqt_endpoint = Blueprint("oqt_endpoint", __name__)


@oqt_endpoint.route("/api/analyze/device/oqt", methods=["POST"])
def analyze():

    return Response(status=200)
