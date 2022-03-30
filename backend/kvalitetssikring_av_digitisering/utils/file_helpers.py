""" Module for file checking methods
"""

import os, errno
from kvalitetssikring_av_digitisering.utils.path_helpers import (
    get_session_image_file,
    get_analysis_dir_image_file,
)


def is_file_empty(file):
    """Method which checks if a file is empty

    Args:
        file (FileStorage): the file to be checked

    Returns:
        bool: True if empty, false otherwise
    """
    file.seek(0, os.SEEK_END)
    if file.tell() == 0:
        file.seek(0)
        return True
    file.seek(0)
    return False


def delete_file(session_id, file_name):
    """Removes all references to a file in a session

    Args:
        session_id (str): id of a session
        file_name (str): name of a file

    """
    # Remove file from image folder
    silentremove(get_session_image_file(session_id, file_name))
    # Remove files from output folder
    scores = ["A", "B", "C"]
    for score in scores:
        silentremove(get_analysis_dir_image_file(session_id, file_name, score))


def silentremove(filename):
    """Silently remove file, only raise exception of something happends during removal.
    If it does not exist, move on.
    src: https://stackoverflow.com/a/10840586

    Args:
        filename (str): path to file
    """
    try:
        os.remove(filename)
    except OSError as error:
        if error.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred
