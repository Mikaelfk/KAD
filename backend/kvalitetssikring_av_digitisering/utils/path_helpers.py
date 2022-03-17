"""Module for simplifying path management.

Contains methods needed for getting paths for various files and folders in sessions.
"""
import os

from kvalitetssikring_av_digitisering.config import Config


def get_session_dir(session_id: str):
    """Method for getting the path to the session dir.

    Args:
        session_id (str): the unique id of a session

    Returns:
        path (str): path to the session dir
    """

    return os.path.join(
        Config.config().get(section="API", option="StorageFolder"), session_id
    )


def get_session_images_dir(session_id: str):
    """Method for getting the path to the session images dir.

    Args:
        session_id (str): the unique id of a session

    Returns:
        path (str): path to the session images dir
    """

    return os.path.join(
        Config.config().get(section="API", option="StorageFolder"),
        session_id,
        "images",
    )


def get_session_outputs_dir(session_id: str):
    """Method for getting the path to the session outputs dir

    Args:
        session_id (str): the unique id of a session

    Returns:
        path (str): path to the session outputs dir
    """

    return os.path.join(
        Config.config().get(section="API", option="StorageFolder"),
        session_id,
        "outputs",
    )


def get_analysis_dir(session_id: str, file_name: str, score: str):
    """Method for getting the path to the analysis dir of an image in a session.

    Args:
        session_id (str): the unique id of a session

    Returns:
        path (str): path to the session analysis dir of the image
    """

    return os.path.join(
        Config.config().get(section="API", option="StorageFolder"),
        session_id,
        "outputs",
        f"{file_name}-analysis",
        score,
    )


def get_session_image_file(session_id: str, file_name: str):
    """Method for getting the path to an image in a session.

    Args:
        session_id (str): the unique id of a session

    Returns:
        path (str): path to the image in a session
    """

    return os.path.join(
        get_session_images_dir(session_id),
        file_name,
    )


def get_session_results_file(session_id: str):
    """Method for getting the path to a sessions result file.

    Args:
        session_id (str): the unique id of a session

    Returns:
        path (str): path to the image in a session
    """

    return os.path.join(
        Config.config().get(section="API", option="StorageFolder"),
        session_id,
        "results.json",
    )


def get_analysis_dir_image_file(session_id: str, file_name: str, score: str):
    """Method for getting the path to an image in its analysis folder.

    Args:
        session_id (str): the unique id of a session

    Returns:
        path (str): path to the image in its analysis folder
    """

    return os.path.join(get_analysis_dir(session_id, file_name, score), file_name)


def get_analysis_dir_image_iqx_result_file(session_id: str, file_name: str, score: str):
    """Method for getting the path to an iqx analysis result in its analysis folder.

    Args:
        session_id (str): the unique id of a session

    Returns:
        path (str): path to the iqx analysis result in its analysis folder
    """

    return os.path.join(
        get_analysis_dir(session_id, file_name, score), "analysis_result.xml"
    )
