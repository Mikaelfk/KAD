"""Module for validate endpoint

This module is for use with Flask, and should therefore not be directly called.
It defines the code for an endpoint that takes an image, checks it with JHove and returns
validity result.
"""

import json
import os

from flask import Blueprint, request
from flask.wrappers import Response
from werkzeug.utils import secure_filename

from ..config import Config
from ..file_validation import jhove_validation

validate_endpoint = Blueprint("validate_endpoint", __name__)


@validate_endpoint.route("/api/validate", methods=["POST"])
def validate():
    """Method for saving and validating incoming image

    Returns:
        A HTTP Respons with corresponding status code and data
    """

    # check if there is a file
    if "file" not in request.files:
        return Response(json.dumps({"error": "no file provided"}), status=400)

    file = request.files["file"]

    # check if the file has a name
    if file.filename == "" or file.filename is None:
        return Response(json.dumps({"error": "invalid file name"}), status=400)

    # check if file has valid extension
    file_ext = os.path.splitext(file.filename)[1]
    if file_ext not in {".jpeg", ".jpg", ".tiff", ".tif"}:
        return Response(json.dumps({"error": "invalid file type"}), status=400)

    # lets go upload time!
    if file:
        filename = secure_filename(file.filename)
        file.save(
            os.path.join(
                Config.config().get(section="API", option="UploadFolder"), filename
            )
        )

        # check file
        validation_output = jhove_validation(
            os.path.join(
                Config.config().get(section="API", option="UploadFolder"), filename
            ),
            Config.config().get(section="JHOVE", option="JhoveInstallPath"),
        )

        # return result
        resp = Response(json.dumps({"isValid": str(validation_output[1])}), status=200)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    else:
        return Response(json.dumps({"error": "unable to validate file"}), 500)
