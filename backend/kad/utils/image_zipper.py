"""Module for zipping all images in a session
"""
import logging
from shutil import make_archive

from kad.utils.path_helpers import get_session_dir, get_session_images_dir
from kad.utils.session_manager import update_session_status


def zip_all_images_in_session(session_id):
    """Method which zips all images in a session with the given session_id

    Args:
        session_id (str): The id of a session
    """

    logging.getLogger().info(
        "Creating zip file of all files in session %s",
        session_id,
    )

    # Sets the session status to zipping
    update_session_status(session_id, "zipping")
    make_archive(
        get_session_images_dir(session_id),
        "zip",
        root_dir=get_session_dir(session_id),
        base_dir="images/",
    )
