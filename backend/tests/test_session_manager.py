import uuid
import os.path
import json
from kvalitetssikring_av_digitisering.config import Config
from kvalitetssikring_av_digitisering.session_manager import create_session

storage_folder_dir = Config.config().get(section="API", option="StorageFolder")


def test_create_session():
    """tests if create_session function works
    """
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
