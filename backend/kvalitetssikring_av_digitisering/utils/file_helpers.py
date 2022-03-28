""" Module for file checking methods
"""

import os


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
