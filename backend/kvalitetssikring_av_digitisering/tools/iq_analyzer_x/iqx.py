"""Module for performing analusis with IQX.

Contains methods for performing single or multiple analyses,
parsing results and saving them in a session
"""

import os
import subprocess

from kvalitetssikring_av_digitisering.config import Config
from kvalitetssikring_av_digitisering.tools.iq_analyzer_x.parser import (
    result_summary_parser,
)
from kvalitetssikring_av_digitisering.utils.json_helpers import (
    json_iqx_add_result,
    json_iqx_set_analysis_failed,
    json_iqx_set_image_tag,
    json_iqx_set_overall_score,
    read_from_json_file,
    write_to_json_file,
    json_get_best_passing_iso_score,
)
from kvalitetssikring_av_digitisering.utils.path_helpers import (
    get_analysis_dir_image_file,
    get_analysis_dir_image_iqx_result_file,
    get_session_dir,
    get_session_image_file,
    get_session_images_dir,
    get_session_results_file,
)
from kvalitetssikring_av_digitisering.utils.metadata_add import add_metadata_to_file
from kvalitetssikring_av_digitisering.utils.session_manager import update_session_status


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
        return False

    return True


def run_iso_analysis(file_name: str, session_id: str):
    """Runs analysis using all three ISO levels on image.

    Args:
        filename (str): name of file to run analysis on
        session_id (str): The session id of the current session
    """

    update_session_status(session_id, "running")

    for specification_level in ["C", "B", "A"]:
        result_data = read_from_json_file(get_session_results_file(session_id))

        # run analysis on image
        result = run_analysis(
            get_analysis_dir_image_file(session_id, file_name, specification_level),
            specification_level,
        )

        # if iqx fails, set result to failed and move on
        if result is False:
            print("uwu iqx machine broke")
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
            print("uwu parser machine broke")
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


def run_before_after_target_analysis(
    before_target_filename: str, after_target_filename: str, session_id
):
    """Method for running analysis for the before and after target usecase.

    Args:
        before_target_filename (str): filename of the first target
        after_target_filename (str): filename of the second target
        session_id (str): the session id of the current session
    """

    # run analysis
    run_iso_analysis(before_target_filename, session_id)
    run_iso_analysis(after_target_filename, session_id)

    # set image tags
    result_data = read_from_json_file(get_session_results_file(session_id))
    result_data = json_iqx_set_image_tag(
        result_data, before_target_filename, "before_target"
    )
    result_data = json_iqx_set_image_tag(
        result_data, after_target_filename, "after_target"
    )

    # set the overall score of the targets
    result_data = json_iqx_set_overall_score(
        result_data,
        before_target_filename,
        str(json_get_best_passing_iso_score(result_data, before_target_filename)),
    )
    result_data = json_iqx_set_overall_score(
        result_data,
        after_target_filename,
        str(json_get_best_passing_iso_score(result_data, after_target_filename)),
    )

    write_to_json_file(get_session_results_file(session_id), result_data)

    session_image_folder = get_session_images_dir(session_id)

    # find name of all image files in session
    image_files = [
        f
        for f in os.listdir(session_image_folder)
        if os.path.isfile(os.path.join(session_image_folder, f))
    ]

    for file_name in image_files:
        add_metadata_to_file(
            get_session_image_file(session_id, file_name),
            get_session_results_file(session_id),
        )

    # set session status as finished
    update_session_status(session_id, "finished")


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
    except FileNotFoundError as exception:
        print(exception)
        return None
