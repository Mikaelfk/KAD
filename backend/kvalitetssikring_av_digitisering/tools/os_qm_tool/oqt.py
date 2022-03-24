"""Module for running analyses with OS QM-Tool

Contains methods for running multiple or single analyses
"""
import os
import subprocess

from kvalitetssikring_av_digitisering.config import Config
from kvalitetssikring_av_digitisering.utils.path_helpers import (
    get_analysis_dir,
    get_analysis_dir_image_file,
    get_session_images_dir,
)
from kvalitetssikring_av_digitisering.utils.session_manager import update_session_status

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def run_analyses_all_images(session_id: str, target_name: str):
    """Method for running analyses on all images in a session

    Args:
        session_id (str): session id of the current session
        target_name (str): image target which is used for analysis
    """
    image_dir = get_session_images_dir(session_id)

    # find name of all image files in session
    image_files = [
        f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))
    ]

    update_session_status(session_id, "running")

    for image_name in image_files:
        run_iso_analysis(image_name, target_name, session_id)

    update_session_status(session_id, "finished")


def run_iso_analysis(image_name: str, target_name: str, session_id: str):
    """Method for running all iso level analyses on a single image

    Args:
        image_name (str): image to be analyzed
        target_name (str): image target which is used for analysis
        session_id (str): session id of the current session
    """
    for specification_level in ["A", "B", "C"]:
        image_path = get_analysis_dir_image_file(
            session_id, image_name, specification_level
        )

        run_analysis(
            image_path,
            target_name,
            os.path.join(
                get_analysis_dir(session_id, image_name, specification_level),
                "result.txt",
            ),
            specification_level,
        )


def run_analysis(
    image_file_path: str, target_name: str, output_file: str, specification_level: str
):
    """Method for running analysis on a single image with a given specification level

    Args:
        image_file_path (str): absolute path to the image which should be analyzed
        target_name (str): image target which is used for analysis
        output_file (str): path to where the result should be saved
        specification_level (str): what specification level the analysis should be

    Returns:
        bool: True if analysis has been run, false otherwis
    """

    if specification_level not in ["A", "B", "C"]:
        return False

    parameter_folder = os.path.join(THIS_DIR, "resources", "parameter_files")
    match target_name:
        case "UTT" | "TE263" | "GTObject" | "GTDevice":
            parameter_file = os.path.join(
                parameter_folder, f"{target_name}_{specification_level}.qmp"
            )
        case _:
            return False

    oqt_executable = os.path.join(
        Config.config().get(section="OS QM-Tool", option="InstallPath"),
        "QMTool.exe",
    )
    try:
        # order of arguments somewhat arbitrary, but chose same as example in manual just in case
        subprocess.run(
            [
                oqt_executable,
                image_file_path,
                parameter_file,
                output_file,
            ],
            timeout=int(
                Config.config().get(section="OS QM-Tool", option="SessionTimeout")
            ),
            check=True,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False

    return True
