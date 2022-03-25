"""Function that modify uploaded files, but stores the original filename in the session root
"""
import uuid
import os
from kvalitetssikring_av_digitisering.utils.path_helpers import (
    get_session_image_file,
    get_analysis_dir,
)
from kvalitetssikring_av_digitisering.utils.json_helpers import write_to_json_file
from kvalitetssikring_av_digitisering.utils.file_helpers import is_file_empty


def save_files(session_id: str, files):
    """Saves the uploaded files with a unique ID and maps the original value to a dict

    Args:
        session_id (str): id of the session
        files (list[FileStorage]): list of uploaded files
    """
    file_names = {}

    # Store files
    for file in files:
        if not is_file_empty(file):
            new_file_name = str(uuid.uuid4())
            file_names.update({new_file_name: str(file.filename)})
            file.save(get_session_image_file(session_id, new_file_name))

    # Store mapped names
    write_to_json_file(os.path.join(get_analysis_dir, "file_names.json"), file_names)
