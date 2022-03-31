"""test for the session_manager module
"""
import os
import shutil
import uuid

from kad.config import Config
from kad.utils.json_helpers import read_from_json_file
from kad.utils.path_helpers import (
    get_analysis_dir,
    get_analysis_dir_image_file,
    get_session_images_dir,
    get_session_outputs_dir,
    get_session_state_file,
)
from kad.utils.session_manager import (
    check_session_exists,
    create_analysis_folders,
    create_session,
    update_session_status,
)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER_DIR = Config.config().get(section="API", option="StorageFolder")

# Makes the StorageFolder directory
os.makedirs(STORAGE_FOLDER_DIR, exist_ok=True)

# Makes a session
SESSION_ID = create_session()


def test_create_session():
    """Tests if create_session function works"""

    # Asserts that the SESSION_ID is a valid uuid
    try:
        uuid.UUID(str(SESSION_ID))
        assert True
    except ValueError:
        assert False

    session_state_file = get_session_state_file(SESSION_ID)

    # Checks that the storage folder exists
    assert os.path.isdir(STORAGE_FOLDER_DIR)

    # Checks that the outputs folder exists
    assert os.path.isdir(get_session_outputs_dir(SESSION_ID))

    # Checks that the images folder exists
    assert os.path.isdir(get_session_images_dir(SESSION_ID))

    # Checks that the state.json file exists
    assert os.path.isfile(session_state_file)

    data = read_from_json_file(session_state_file)
    assert data["status"] == "created"


def test_create_analysis_folders():
    """Test the create_analysis_folders function"""
    # Define constants for image name and image analysis folder
    test_image_name = "test_image.jpg"

    # Sets the source and destination path for the test image
    src = os.path.join(THIS_DIR, "test_pictures", test_image_name)
    dst = get_session_images_dir(SESSION_ID)

    # Copies the image to the destination path
    shutil.copy(src, dst)

    # Creates the analysis folders
    create_analysis_folders(SESSION_ID)

    iso_scores = ["A", "B", "C"]

    for score in iso_scores:
        assert os.path.isdir(get_analysis_dir(SESSION_ID, test_image_name, score))

        assert os.path.isfile(
            get_analysis_dir_image_file(SESSION_ID, test_image_name, score)
        )


def test_check_session_exists_postive():
    """Tests the check_session_exists function when SESSION_ID is correct"""
    assert check_session_exists(SESSION_ID)


def test_check_session_exists_negative():
    """Tests the check_session_exists function when SESSION_ID is not correct"""
    assert not check_session_exists("wrong_SESSION_ID_:)")


def test_update_session_status():
    """Sets the session status in state.json to finished and asserts if the change was made"""
    update_session_status(SESSION_ID, "finished")

    data = read_from_json_file(get_session_state_file(SESSION_ID))
    assert data["status"] == "finished"
