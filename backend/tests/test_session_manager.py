import uuid
import os.path
import json
from kvalitetssikring_av_digitisering.config import Config
from kvalitetssikring_av_digitisering.session_manager import create_session, check_session_exists, update_session_status

storage_folder_dir = Config.config().get(section="API", option="StorageFolder")


def test_create_session():
    """tests if create_session function works
    """
    # Makes the StorageFolder directory
    os.makedirs(storage_folder_dir, exist_ok=True)

    session_id = create_session()

    # Asserts that the session_id is a valid uuid
    try:
        uuid.UUID(str(session_id))
        assert True
    except ValueError:
        assert False

    session_state_file = os.path.join(
        storage_folder_dir, session_id, "state.json")

    # Checks that the storage folder exists
    assert os.path.isdir(storage_folder_dir)

    # Checks that the outputs folder exists
    assert os.path.isdir(os.path.join(
        storage_folder_dir, session_id, "outputs"))

    # Checks that the images folder exists
    assert os.path.isdir(os.path.join(
        storage_folder_dir, session_id, "images"))

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


def test_check_session_exists_postive():
    session_id = create_session()
    assert check_session_exists(session_id)


def test_check_session_exists_negative():
    assert not check_session_exists("wrong_session_id_:)")


def test_update_session_status():
    session_id = create_session()

    update_session_status(session_id, "finished")

    session_state_file = os.path.join(
        storage_folder_dir, session_id, "state.json")

    with open(session_state_file, "a+", encoding="UTF-8") as json_file:
        json_file.seek(0)

        if os.path.getsize(session_state_file) > 0:
            data = json.load(json_file)
        else:
            data = {}

        # Checks that the status in state.json is "created"
        assert data["status"] == "finished"
