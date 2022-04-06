"""Module for performing analysis with IQX.

Contains methods for performing single or multiple analyses,
parsing results and saving them in a session
"""
import logging
import os
import subprocess

from kad.config import Config
from kad.tools.iq_analyzer_x.parser import result_summary_parser
from kad.utils.json_helpers import (
    json_iqx_add_result,
    json_iqx_set_analysis_failed,
    read_from_json_file,
    write_to_json_file,
)
from kad.utils.path_helpers import (
    get_analysis_dir_image_file,
    get_analysis_dir_image_iqx_result_file,
    get_session_results_file,
)


def run_analysis(image_file_path: str, specification_level: str):
    """Runs analysis on one image of given specification level.

    Args:
        image_file_path (str): The path to the file which should be analyzed
        specification_level (str): Specification ISO level the image should be tested against

    Returns:
        bool: true if analysis passed, false otherwise
    """

    match specification_level:
        case "A":
            specification_number = 1
        case "B":
            specification_number = 2
        case "C":
            specification_number = 3
        case _:
            return False

    logging.getLogger().info(
        "Running analysis on file %s with specification level %s",
        image_file_path,
        specification_level,
    )

    # static args
    iqx_executable = os.path.join(
        Config.config().get(section="IQ ANALYZER X", option="InstallPath"),
        "iQ-Analyzer-X.exe",
    )
    reference = "--reference='-1'"
    utt = "--utt"
    exif = "--preferExif"
    settings_id = "--settingsID=1"

    # variable args
    image_file = os.path.normpath(f"{image_file_path}")
    specification = f"--specification='{specification_number}'"

    try:
        # order of arguments somewhat arbitrary, but chose same as example in manual just in case
        subprocess.run(
            [
                iqx_executable,
                image_file,
                settings_id,
                reference,
                utt,
                specification,
                exif,
            ],
            timeout=int(
                Config.config().get(section="IQ ANALYZER X", option="SessionTimeout")
            ),
            check=True,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        logging.getLogger().warning(
            "Failed to run analysis on %s with specification level %s",
            image_file_path,
            specification_level,
        )
        return False

    return True


def run_iso_analysis(file_name: str, session_id: str):
    """Runs analysis using all three ISO levels on image.

    Args:
        filename (str): name of file to run analysis on
        session_id (str): The session id of the current session
    """

    logging.getLogger().info(
        "Starting iso analysis of file %s in session %s", file_name, session_id
    )

    for specification_level in ["C", "B", "A"]:
        result_data = read_from_json_file(get_session_results_file(session_id))

        # run analysis on image
        result = run_analysis(
            get_analysis_dir_image_file(session_id, file_name, specification_level),
            specification_level,
        )

        # if iqx fails, set result to failed and move on
        if result is False:
            logging.getLogger().warning(
                """IQX failed while analyzing file %s in session %s.
                Setting analysis result to failed""",
                file_name,
                session_id,
            )

            result_data = json_iqx_set_analysis_failed(
                result_data, file_name, specification_level
            )
            write_to_json_file(get_session_results_file(session_id), result_data)
            continue

        # parse results from analysis
        analysis_results = parse_results(
            get_analysis_dir_image_iqx_result_file(
                session_id, file_name, specification_level
            )
        )

        # if parsing fails, iqx probably also fails,
        # so set result to failed and move on
        if analysis_results is None:
            logging.getLogger().warning(
                """Parser failed to parse data from analysis on file %s in session %s.
                Setting analysis result to failed!""",
                file_name,
                session_id,
            )

            result_data = json_iqx_set_analysis_failed(
                result_data, file_name, specification_level
            )
            write_to_json_file(get_session_results_file(session_id), result_data)
            continue

        # add result to data
        result_data = json_iqx_add_result(
            result_data, file_name, specification_level, analysis_results
        )

        write_to_json_file(get_session_results_file(session_id), result_data)


def parse_results(result_file_path: str):
    """Method for parsing the results of a IQ Analyzer X analysis.

    Args:
        result_file_path(str): absolute path to a file that contains the results of an analyis

    Returns:
        dict | None: returns the parsed results as a dict or None if no results were found
    """

    try:
        parsed_result = result_summary_parser(result_file_path)

        return parsed_result
    except FileNotFoundError:
        logging.getLogger().warning(
            "Parses was not able to find file %s", result_file_path
        )

        return None
