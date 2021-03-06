"""Module for running analyses with OS QM-Tool

Contains methods for running multiple or single analyses
"""
import logging
import os
import subprocess

from kad.config import Config
from kad.tools.os_qm_tool.parser import result_summary_parser
from kad.utils.json_helpers import (
    json_iqx_add_result,
    json_iqx_set_analysis_failed,
    read_from_json_file,
    write_to_json_file,
)
from kad.utils.path_helpers import (
    get_analysis_dir,
    get_analysis_dir_image_file,
    get_analysis_dir_image_oqt_result_file,
    get_session_results_file,
)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


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

    logging.getLogger().info(
        "Running analysis on file %s with specification level %s",
        image_file_path,
        specification_level,
    )

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
    except subprocess.CalledProcessError as err:
        if (err.returncode) != 2:
            # If exit code is 2, it means that the result of the analysis did not pass,
            # but the analysis was done, so continue
            logging.getLogger().warning(
                "Failed to run analysis on %s with specification level %s",
                image_file_path,
                specification_level,
            )
            return False
    except subprocess.TimeoutExpired:
        logging.getLogger().warning(
            "Failed to run analysis on %s with specification level %s",
            image_file_path,
            specification_level,
        )
        return False

    return True


def run_iso_analysis(file_name: str, target_name: str, session_id: str):
    """Method for running all iso level analyses on a single image

    Args:
        file_name (str): image to be analyzed
        target_name (str): image target which is used for analysis
        session_id (str): session id of the current session
    """

    logging.getLogger().info(
        "Starting iso analysis of file %s in session %s", file_name, session_id
    )

    for specification_level in ["A", "B", "C"]:
        image_path = get_analysis_dir_image_file(
            session_id, file_name, specification_level
        )

        result = run_analysis(
            image_path,
            target_name,
            os.path.join(
                get_analysis_dir(session_id, file_name, specification_level),
                "result.txt",
            ),
            specification_level,
        )

        result_data = read_from_json_file(get_session_results_file(session_id))

        # if os qm tool fails, set result to failed and move on
        if result is False:
            logging.getLogger().warning(
                "OQT failed while analyzing file %s in session %s. Setting analysis result to failed",
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
            get_analysis_dir_image_oqt_result_file(
                session_id, file_name, specification_level
            )
        )

        # if parsing fails, os qm tool probably also fails,
        # so set result to failed and move on
        if analysis_results is None:
            logging.getLogger().warning(
                "Parser failed to parse data from analysis on file %s in session %s. Setting analysis result to failed!",
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
    """Method for parsing the results

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
