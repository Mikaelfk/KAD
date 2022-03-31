"""Function that modify uploaded files, but stores the original filename in the session root
"""
import uuid
import pathlib
from werkzeug.utils import secure_filename
from kad.utils.path_helpers import (
    get_session_image_file,
)
from kad.utils.file_helpers import is_file_empty


def save_uploaded_files(session_id: str, files, file_names=None):
    """Saves the uploaded files with a unique name.
    For example:
    - filename.jpeg
    - filename_1.jpeg
    - filename_2.jpeg

    Args:
        session_id (str): id of the session
        files (list[FileStorage]): list of uploaded files
        file_names (list[str]): list of all file names

    Returns:
        str: filename to the last imported file (used to get target image)
    """
    if file_names is None:
        file_names = []

    # Store files
    for file in files:
        if is_file_empty(file):
            continue

        # Secure filename parses the filename and return a secure version.
        # This may result in an ampty filename.
        # If that is the case, we create a random uuid of 6 chars
        file_name = secure_filename(file.filename)
        if file_name == "":
            file_name = str(uuid.uuid4())[:6]

        # Check for dupliates
        i = 1
        new_file_name = file_name
        while new_file_name in file_names:
            # Add _n to file if duplicate
            # file.jpeg -> file_n.jpeg
            file_name_path = pathlib.Path(file_name)
            new_file_name = f"{file_name_path.stem}_{i}{file_name_path.suffix}"
            i += 1

        # Save file
        file.save(get_session_image_file(session_id, new_file_name))
        file_names.append(new_file_name)

    # Store mapped names
    if len(file_names) > 0:
        return file_names[-1]
    return ""
