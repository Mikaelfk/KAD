"""Module for validating image files with JHOVE.

Requires a valid JHOVE installation to work.
"""

import os


def jhove_validation(url, jhove_path):
    """File validation using JHOVE.

    Args:
        url (str): the path of the image which should be validated
        jhove_path (str): the path to the JHOVE installation

    Returns:
        str: output with all the metadata
        bool: True if successful, False otherwise
    """

    os.chdir(jhove_path)

    # Check if operating system is posix or windows
    if os.name == "posix":
        jhove_command = "./jhove"
    else:
        jhove_command = "jhove.bat"
        url = url.replace("/", "\\")

    # Runs the file validation and saves the output to a variable
    if url.lower().endswith(".jpg") or url.lower().endswith(".jpeg"):
        stream = os.popen(jhove_command + " -m JPEG-hul -kr " + '"' + url + '"')
    elif url.lower().endswith(".tiff") or url.lower().endswith(".tif"):
        stream = os.popen(jhove_command + " -m TIFF-hul -kr " + '"' + url + '"')
    else:
        return "Filetype not valid", None
    output = stream.read()

    # Checks if the validation was successful
    if "Status: Well-Formed and valid" not in output:
        status = False
    else:
        status = True

    return output, status
