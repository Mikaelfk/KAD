"""Module for validating image files with JHOVE.

Requires a valid JHOVE installation to work.
"""

import logging
import os

from kad.config import Config

jhove_path = Config.config().get(section="JHOVE", option="JhoveInstallPath")


def jhove_validation(url):
    """File validation using JHOVE.

    Args:
        url (str): the path of the image which should be validated

    Returns:
        str: output with all the metadata
        bool: True if successful, False otherwise
    """

    # Check if operating system is posix or windows
    if os.name == "posix":
        jhove_command = os.path.join(jhove_path, "jhove")
    else:
        jhove_command = os.path.join(jhove_path, "jhove.bat")
        url = url.replace("/", "\\")

    # Runs the file validation and saves the output to a variable
    if url.lower().endswith(".jpg") or url.lower().endswith(".jpeg"):
        logging.getLogger().info("Validating JPEG file %s with JHOVE", url)

        stream = os.popen(jhove_command + " -m JPEG-hul -kr " + '"' + url + '"')
    elif url.lower().endswith(".tiff") or url.lower().endswith(".tif"):
        logging.getLogger().info("Validating TIFF file %s with JHOVE", url)

        stream = os.popen(jhove_command + " -m TIFF-hul -kr " + '"' + url + '"')
    else:
        logging.getLogger().warning("File %s can not be validated with JHOVE", url)

        return "Filetype not valid", False
    output = stream.read()

    # Checks if the validation was successful
    if "Status: Well-Formed and valid" not in output:
        status = False
    else:
        status = True

    return output, status
