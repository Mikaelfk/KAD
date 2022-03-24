import json
from flask import Blueprint, request
from flask.wrappers import Response

from kvalitetssikring_av_digitisering.tools.os_qm_tool.oqt import (
    run_analyses_all_images,
    run_analysis,
)
from kvalitetssikring_av_digitisering.utils.path_helpers import get_session_image_file
from kvalitetssikring_av_digitisering.utils.session_manager import (
    create_analysis_folders,
    create_session,
)

oqt_endpoint = Blueprint("oqt_endpoint", __name__)


@oqt_endpoint.route("/api/analyze/device/oqt", methods=["POST"])
def analyze():
    target = request.args.get("target")

    match target:
        case "UTT" | "TE263" | "GTObject" | "GTDevice":
            print("Target which is used: " + target)
            files = request.files.getlist("files")
            session_id = create_session()

            for file in files:
                file.save(get_session_image_file(session_id, str(file.filename)))

            create_analysis_folders(session_id)

            run_analyses_all_images(session_id, target)

            return Response(json.dumps({"session_id": str(session_id)}), status=200)

        case None | "":
            return Response(json.dumps({"error:": "no target specified"}), status=400)

        case _:
            return Response(json.dumps({"error": "invalid target"}), status=400)
