from flask import Blueprint, request
from flask.wrappers import Response
import json
import os

from ..config import Config
from ..tools.iq_analyzer_x.iqx import run_analysis
from ..session_manager import create_session, create_analysis_folders

iqx_endpoint = Blueprint("iqx_endpoint", __name__)


@iqx_endpoint.route("/api/analyze/device/iqx", methods=["POST"])
def analyze():
    target = request.args.get("target")

    # make sure it's a valid target
    match target:
        case "UTT":
            print("uwu")
            session_id = create_session()
            before_target = request.files["before_target"]
            after_target = request.files["after_target"]
            #files = request.files["files"]


            before_target_path = os.path.join(
                Config.config().get(section="API", option="StorageFolder"), session_id , "images" , before_target.filename
            )      
            after_target_path = os.path.join(
                Config.config().get(section="API", option="StorageFolder"), session_id , "images" , after_target.filename
            )

            before_target.save(before_target_path)
            after_target.save(after_target_path)

            create_analysis_folders(session_id)
           
            scores = ["C", "B", "A"] 

            i = 0
            while(i < len(scores) and run_analysis(before_target_path ,scores[i]) and run_analysis(after_target_path, scores[i])):
                i += 1


        case None | "":
            return Response(json.dumps({"error:": "no target specified"}), status=400)

        case _:
            return Response(json.dumps({"error": "invalid target"}), status=400)

    return Response(status=200)
