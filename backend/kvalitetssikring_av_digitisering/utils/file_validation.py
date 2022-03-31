"""Module for validating image files with JHOVE.

Requires a valid JHOVE installation to work.
"""

import os

from kvalitetssikring_av_digitisering.config import Config

jhove_path = Config.config().get(section="JHOVE", option="JhoveInstallPath")
print(jhove_path)


def jhove_validation(url):
    """File validation using JHOVE.

    Args:
        url (str): the path of the image which should be validated

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
        return "Filetype not valid", False
    output = stream.read()

    # Checks if the validation was successful
    if "Status: Well-Formed and valid" not in output:
        status = False
    else:
        status = True

    return output, status
