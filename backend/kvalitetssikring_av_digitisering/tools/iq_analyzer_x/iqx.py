"""Moodule for performing analusis with IQX.

Contains methods for performing single or multiple analyses,
parsing results and saving them in a session
"""

import json
import os
import subprocess
from collections import defaultdict

from ...config import Config
from ...session_manager import update_session_status

from .parser import result_summary_parser


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
        timeout=120,
        check=False,
    )

    return True


def run_analyses(
    before_target_filename: str, after_target_filename: str, session_id: str
):
    """Runs analysis using all three ISO levels on both before and after target.

    Args:
        before_target_path (str): The target which is scanned at the start of an image batch
        after_target_path (str): The target which is scanend at the end of an image batch
        session_id (str): The session id of the current session
    """

    for score in ["C", "B", "A"]:
        before_target_path = os.path.join(
            Config.config().get(section="API", option="StorageFolder"),
            session_id,
            "outputs",
            before_target_filename + "-analysis",
            score,
        )

        after_target_path = os.path.join(
            Config.config().get(section="API", option="StorageFolder"),
            session_id,
            "outputs",
            after_target_filename + "-analysis",
            score,
        )

        # duplicated twice, but eh might be fine

        # run for before target
        run_analysis(os.path.join(before_target_path, before_target_filename), score)
        parsed_results_before = parse_results(
            os.path.join(before_target_path, "analysis_result.xml")
        )

        if parsed_results_before is not None:
            save_results(
                session_id,
                before_target_filename,
                score,
                parsed_results_before,
                "before_target",
            )

        # run for after target
        run_analysis(os.path.join(after_target_path, after_target_filename), score)
        parsed_results_after = parse_results(
            os.path.join(after_target_path, "analysis_result.xml")
        )

        if parsed_results_after is not None:
            save_results(
                session_id,
                after_target_filename,
                score,
                parsed_results_after,
                "after_target",
            )

    update_session_status(session_id, "Finished")


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


def save_results(
    session_id: str,
    filename: str,
    specification_level: str,
    results: dict,
    target_order: str,
):
    """Method for saving the results after an analysis.

    This method will save the results in the results file in a session

    Args:
        session_id (str): Unique session id
        filename (str): name of analyzed file
        specification_level (str): specification level used when analyzing
        results (dict): parsed analysis results
        target_order (str): which target (before, middle, after ...)
    """

    session_results_file = os.path.join(
        Config.config().get(section="API", option="StorageFolder"),
        session_id,
        "results.json",
    )

    # get data from file
    with open(session_results_file, "a+", encoding="UTF-8") as json_file:
        json_file.seek(0)

        if os.path.getsize(session_results_file) > 0:
            data = json.load(json_file)
        else:
            data = {}

    # update data
    data = defaultdict(dict, data)
    data[str(filename)]["target_order"] = target_order
    data[str(filename)][str(specification_level)] = results

    # write new data to file
    with open(session_results_file, "w+", encoding="UTF-8") as json_file:
        json_file.write(json.dumps(dict(data)))
