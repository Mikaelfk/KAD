"""Module for zipping all images in a session
"""
import os
from shutil import make_archive
from kvalitetssikring_av_digitisering.utils.path_helpers import get_session_dir
from kvalitetssikring_av_digitisering.utils.session_manager import update_session_status


def zip_all_images_in_session(session_id):
    """Method which zips all images in a session with the given session_id

    Args:
        session_id (str): The id of a session
    """

    # Sets the session status to zipping
    update_session_status(session_id, "zipping")
    make_archive(
        os.path.join("storage", session_id, "images"),
        "zip",
        root_dir=get_session_dir(session_id),
        base_dir="images/",
    )
