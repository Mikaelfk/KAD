"""test for the session_manager module
"""
import uuid
import os.path
import json
import shutil

from kvalitetssikring_av_digitisering.config import Config
from kvalitetssikring_av_digitisering.session_manager import (
    create_session,
    check_session_exists,
    update_session_status,
    create_analysis_folders
)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER_DIR = Config.config().get(section="API", option="StorageFolder")
# Makes a session
SESSION_ID = create_session()

# Makes the StorageFolder directory
os.makedirs(STORAGE_FOLDER_DIR, exist_ok=True)


def test_create_session():
    """Tests if create_session function works
    """

    # Asserts that the SESSION_ID is a valid uuid
    try:
        uuid.UUID(str(SESSION_ID))
        assert True
    except ValueError:
        assert False

    session_state_file = os.path.join(
        STORAGE_FOLDER_DIR, SESSION_ID, "state.json")

    # Checks that the storage folder exists
    assert os.path.isdir(STORAGE_FOLDER_DIR)

    # Checks that the outputs folder exists
    assert os.path.isdir(os.path.join(
        STORAGE_FOLDER_DIR, SESSION_ID, "outputs"))

    # Checks that the images folder exists
    assert os.path.isdir(os.path.join(
        STORAGE_FOLDER_DIR, SESSION_ID, "images"))

    # Checks that the state.json file exists
    assert os.path.isfile(session_state_file)

    with open(session_state_file, "a+", encoding="UTF-8") as json_file:
        json_file.seek(0)

        if os.path.getsize(session_state_file) > 0:
            data = json.load(json_file)
        else:
            data = {}

        # Checks that the status in state.json is "created"
        assert data["status"] == "created"


def test_create_analysis_folders():
    """Test the create_analysis_folders function
    """
    # Define constants for image name and image analysis folder
    test_image_name = "test_image.jpg"
    test_image_analysis_path = test_image_name + "-analysis"

    # Sets the source and destination path for the test image
    src = os.path.join(THIS_DIR, "test_pictures", test_image_name)
    dst = os.path.join(STORAGE_FOLDER_DIR, SESSION_ID,
                       "images")

    # Copies the image to the destination path
    shutil.copy(src, dst)

    # Creates the analysis folders
    create_analysis_folders(SESSION_ID)

    iso_scores = ["A", "B", "C"]

    for score in iso_scores:
        assert os.path.isdir(os.path.join(
            STORAGE_FOLDER_DIR, SESSION_ID, "outputs", test_image_analysis_path, score))
        assert os.path.isfile(os.path.join(
            STORAGE_FOLDER_DIR, SESSION_ID, "outputs", test_image_analysis_path, score, test_image_name))


def test_check_session_exists_postive():
    """Tests the check_session_exists function when SESSION_ID is correct
    """
    assert check_session_exists(SESSION_ID)


def test_check_session_exists_negative():
    """Tests the check_session_exists function when SESSION_ID is not correct
    """
    assert not check_session_exists("wrong_SESSION_ID_:)")


def test_update_session_status():
    """Sets the session status in state.json to finished and asserts if the change was made
    """
    update_session_status(SESSION_ID, "finished")

    session_state_file = os.path.join(
        STORAGE_FOLDER_DIR, SESSION_ID, "state.json")

    with open(session_state_file, "a+", encoding="UTF-8") as json_file:
        json_file.seek(0)

        if os.path.getsize(session_state_file) > 0:
            data = json.load(json_file)
        else:
            data = {}

        # Checks that the status in state.json is "created"
        assert data["status"] == "finished"
