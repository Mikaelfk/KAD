"""Module for downloading images in a session.

Contains one endpoint which can be used to download all images or one image if a query is given
"""
import json
import os

from flask import Blueprint, request, send_from_directory
from flask.wrappers import Response
from kad.utils.path_helpers import get_session_dir, get_session_images_dir
from kad.utils.session_manager import check_session_exists, get_session_status
from werkzeug.utils import secure_filename

download_endpoint = Blueprint("download_endpoint", __name__)


@download_endpoint.route("/api/download/<session_id>", methods=["GET"])
def download_images(session_id):
    """An endpoint for downloading images in a session

    Args:
        session_id (str): the id of a session

    Returns:
        Response: the response given is a zip file or an image file
    """

    if not check_session_exists(session_id):
        return Response(json.dumps({"error": "session does not exist"}), status=404)

    if get_session_status(session_id)[0] != "finished":
        return Response(json.dumps({"error": "session is not finished"}), status=400)

    file_name = request.args.get("file_name")
    if file_name is None:
        return send_from_directory(
            get_session_dir(session_id), "images.zip", as_attachment=True
        )

    file_path = os.path.join(
        get_session_images_dir(session_id), secure_filename(file_name)
    )
    if not os.path.isfile(file_path):
        return Response(json.dumps({"error": "image does not exist"}), status=404)

    return send_from_directory(
        get_session_images_dir(session_id),
        secure_filename(file_name),
        as_attachment=True,
    )
