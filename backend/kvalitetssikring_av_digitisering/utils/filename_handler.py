"""Function that modify uploaded files, but stores the original filename in the session root
"""
import uuid
import os
from kvalitetssikring_av_digitisering.utils.path_helpers import (
    get_session_dir,
    get_session_image_file,
)
from kvalitetssikring_av_digitisering.utils.json_helpers import write_to_json_file
from kvalitetssikring_av_digitisering.utils.file_helpers import is_file_empty
from kvalitetssikring_av_digitisering.utils.json_helpers import read_from_json_file

# CONST
FILE_NAME_FILE = "file_names.json"


def save_uploaded_files(session_id: str, files):
    """Saves the uploaded files with a unique ID and maps the original value to a dict

    Args:
        session_id (str): id of the session
        files (list[FileStorage]): list of uploaded files
    """
    json_file, file_names = get_file_names(session_id)

    # Store files
    for file in files:
        if not is_file_empty(file):
            new_file_name = str(uuid.uuid4())
            file_names.update({new_file_name: str(file.filename)})
            file.save(get_session_image_file(session_id, new_file_name))

    # Store mapped names
    write_to_json_file(json_file, file_names)
    return file_names


def get_original_filename(session_id: str, filename: str):
    """Get the original filename

    Args:
        session_id (str): the id of a session
        filename (str): uuid of an image

    Returns:
        str: original filename
    """
    _, file_names = get_file_names(session_id)

    if isinstance(file_names, dict):
        return file_names.get(filename)
    return None


def get_file_names(session_id):
    """Get the file_names for a session

    Args:
        session_id (str): the id of a session

    Returns:
        str: path to json file
        dict | none: file names as a dict
    """
    json_file = os.path.join(get_session_dir(session_id), FILE_NAME_FILE)
    return json_file, read_from_json_file(json_file)
