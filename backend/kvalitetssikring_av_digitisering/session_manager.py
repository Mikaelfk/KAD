"""Module for managing sessions.

Contains several methods for creating, updating and modifying sessions.
"""
import json
import os
import uuid

from .config import Config

#const
STATE = "STATE.json"

def create_session():
    """Method for creating a sessions.

    Returns:
        str: the unique id of the created session
    """

    # gen id for session
    session_id = str(uuid.uuid4())

    # create session dir
    root_folder = Config.config().get(section="API", option="StorageFolder")
    session_dir = os.path.join(root_folder, session_id)
    os.mkdir(session_dir)

    # create folder structure
    os.mkdir(os.path.join(session_dir, "results"))
    os.mkdir(os.path.join(session_dir, "images"))
    os.mkdir(os.path.join(session_dir, "outputs"))

    update_session_status(session_id, "created")

    return session_id


def create_analysis_folders(session_id):
    """Method for creating analysis folders in a session.

    Will look for images in a session, create folders for them,
    and hard-links the image to the folder so it's available there.

    Args:
        session_id (str): the unique id of the session
    """

    session_image_folder = os.path.join(
        Config.config().get(section="API", option="StorageFolder"), session_id, "images"
    )

    session_output_folder = os.path.join(
        Config.config().get(section="API", option="StorageFolder"),
        session_id,
        "outputs",
    )

    # find name of all image files in session
    image_files = [
        f
        for f in os.listdir(session_image_folder)
        if os.path.isfile(os.path.join(session_image_folder, f))
    ]

    # check if directory exsists, and if not: create it
    for file_name in image_files:
        analysis_dir = os.path.join(session_output_folder, file_name + "-analysis")

        if not os.path.isdir(analysis_dir):
            os.mkdir(analysis_dir)

            image_src = os.path.join(session_image_folder, file_name)
            image_dest = os.path.join(
                session_output_folder, file_name + "-analysis", file_name
            )

            os.link(image_src, image_dest)


def update_session_status(session_id, status):
    """Method for updating the status of a session.

    Args:
        session_id (str): the unique id of the session
        status (str): the new status to update to
    """
    session_folder = os.path.join(
        Config.config().get(section="API", option="StorageFolder"), session_id
    )

    # open state file and update json
    with open(
        os.path.join(session_folder, STATE), "w+", encoding="UTF-8"
    ) as json_file:
        if os.stat(os.path.join(session_folder, STATE)).st_size == 0:
            data = {}
        else:
            data = json.load(json_file)

        data["status"] = status

        json_file.write(json.dumps(data))


def check_session_exists(session_id):
    """Method for checking if a session exists.

    Args:
        session_id (str): unique id of the session
    """

    session_folder = os.path.join(
        Config.config().get(section="API", option="StorageFolder"), session_id
    )

    state_file = os.path.join(session_folder, STATE)

    return os.path.isdir(session_folder) or os.path.exists(state_file)
