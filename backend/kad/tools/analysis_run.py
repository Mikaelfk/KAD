"""Module for starting ISO 19264 analysis for device or object level targets.
"""

import logging
import os

import kad.tools.iq_analyzer_x.iqx as iqx
import kad.tools.os_qm_tool.oqt as oqt
from kad.utils.file_validation import jhove_validation
from kad.utils.image_zipper import zip_all_images_in_session
from kad.utils.json_helpers import (
    json_get_best_passing_iso_score,
    json_iqx_set_image_tag,
    json_set_overall_score,
    json_set_validation,
    read_from_json_file,
    write_to_json_file,
)
from kad.utils.metadata_add import add_metadata_to_file
from kad.utils.path_helpers import (
    get_session_dir,
    get_session_image_file,
    get_session_results_file,
)
from kad.utils.session_manager import update_session_status


def run_device_analysis(
    before_target_filename: str,
    after_target_filename: str,
    session_id: str,
    iqes: str,
    target: str,
):
    """Method for running analysis for the before and after device target usecase.

    Args:
        before_target_filename (str): filename of the first target
        after_target_filename (str): filename of the second target
        session_id (str): the session id of the current session
        iqes (str): the iqes to use (IQX or OQT)
        target (str): the target to use (only relevant for OQT, IQX can only do UTT)
    """
    update_session_status(session_id, "running")

    ## setup

    # find name of all image files in session
    session_image_folder = get_session_dir(session_id)
    image_files = [
        f
        for f in os.listdir(session_image_folder)
        if os.path.isfile(os.path.join(session_image_folder, f))
    ]

    # empty dict to put results in
    result_data = {}

    ## file validation
    logging.getLogger().info(
        "Starting file validation on files in session %s",
        session_id,
    )

    # validate before analysis
    validation_result, file_name = validate_files(session_id, image_files, "after")
    if not validation_result:
        update_session_status(session_id, f"failed on validating {file_name}")
        return

    ## analyze tiem
    logging.getLogger().info(
        "Starting before/after target analysis on files %s and %s respectively in session %s.",
        before_target_filename,
        after_target_filename,
        session_id,
    )

    match iqes:
        case "IQX":
            iqx.run_iso_analysis(before_target_filename, session_id)
            iqx.run_iso_analysis(after_target_filename, session_id)
        case "OQT":
            oqt.run_iso_analysis(before_target_filename, target, session_id)
            oqt.run_iso_analysis(before_target_filename, target, session_id)

    ## image tags
    logging.getLogger().info(
        "Setting tags targets in session %s",
        session_id,
    )

    # set image tags
    result_data = read_from_json_file(get_session_results_file(session_id))
    result_data = json_iqx_set_image_tag(
        result_data, before_target_filename, "before_target"
    )
    result_data = json_iqx_set_image_tag(
        result_data, after_target_filename, "after_target"
    )

    logging.getLogger().info(
        "Setting the overall score of targets in session %s",
        session_id,
    )

    ## set the overall score
    result_data = json_set_overall_score(
        result_data,
        before_target_filename,
        str(json_get_best_passing_iso_score(result_data, before_target_filename)),
    )
    result_data = json_set_overall_score(
        result_data,
        after_target_filename,
        str(json_get_best_passing_iso_score(result_data, after_target_filename)),
    )
    write_to_json_file(get_session_results_file(session_id), result_data)

    ## add metadata
    logging.getLogger().info(
        "Adding metadata to all files in session %s",
        session_id,
    )
    add_metadata(session_id, image_files)

    ## validate after added metadata
    validation_result, file_name = validate_files(session_id, image_files, "after")
    if not validation_result:
        update_session_status(session_id, f"failed on validating {file_name}")
        return

    ## zip time
    zip_all_images_in_session(session_id)

    ## finito
    update_session_status(session_id, "finished")


def run_object_analysis(
    session_id: str,
    iges: str,
    target: str,
):
    print("not ready")


def add_metadata(session_id: str, image_files: list[str]):
    """Add metadata to image_files in a session.

    Args:
        session_id (str): id of session
        image_files (list[str]): filenames to add metadata to
    """

    for file_name in image_files:
        add_metadata_to_file(
            get_session_image_file(session_id, file_name),
            read_from_json_file(get_session_results_file(session_id)),
        )


def validate_files(session_id: str, image_files: list[str], order: str):
    """Validates image_files in a session

    Args:
        session_id (str): id of session
        image_files (list[str]): filenames to add metadata to
        order (str): which order the validation is (before/after)

    Returns:
        bool: true if all files validated successfully, false if one failed
        str | None: name of file it failed on, or nothing if all successful
    """

    for file_name in image_files:
        # do validation
        _, validation = jhove_validation(get_session_image_file(session_id, file_name))
        # if one of the files are invalid, we just kill session
        if not validation:
            return False, file_name
        # get updated result data just in case something funny has happened
        result_data = read_from_json_file(get_session_results_file(session_id))
        # add validation result
        result_data = json_set_validation(result_data, file_name, order, validation)
        # save updated result data
        write_to_json_file(get_session_results_file(session_id), result_data)

    return True, None
