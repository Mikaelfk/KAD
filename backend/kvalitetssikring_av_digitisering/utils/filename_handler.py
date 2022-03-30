"""Function that modify uploaded files, but stores the original filename in the session root
"""
import uuid
from kvalitetssikring_av_digitisering.utils.path_helpers import (
    get_session_image_file,
)
from kvalitetssikring_av_digitisering.utils.file_helpers import is_file_empty


def save_uploaded_files(session_id: str, files, file_names=None):
    """Saves the uploaded files with a unique name

    Args:
        session_id (str): id of the session
        files (list[FileStorage]): list of uploaded files

    Returns:
        str: filename to the last imported file (used to get target image)
    """
    if file_names is None:
        file_names = []

    # Store files
    for file in files:
        if not is_file_empty(file):
            file_name = file.filename

            # Check for dupliates
            while file_name in file_names:
                r_id = str(uuid.uuid4())[:4]
                file_name = f"{r_id}-{file_name}"

            # Save file
            file.save(get_session_image_file(session_id, file_name))
            file_names.append(file_name)

    # Store mapped names
    if len(file_names) > 0:
        return file_names[-1]
    return ""
