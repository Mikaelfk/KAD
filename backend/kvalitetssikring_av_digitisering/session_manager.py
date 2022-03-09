import json
import os
import uuid

from .config import Config


def create_session():
    # gen id for session
    id = str(uuid.uuid4())

    # create session dir
    rootFolder = Config.config().get(section="API", option="StorageFolder")
    dir = os.path.join(rootFolder, id)
    os.mkdir(dir)

    # create folder structure
    os.mkdir(os.path.join(dir, "results"))
    os.mkdir(os.path.join(dir, "images"))
    os.mkdir(os.path.join(dir, "outputs"))

    update_session_status(id, "created")

    return id


def create_analysis_folders(id):
    sessionImageFolder = os.path.join(
        Config.config().get(section="API", option="StorageFolder"), id, "images"
    )

    sessionOutputFolder = os.path.join(
        Config.config().get(section="API", option="StorageFolder"), id, "outputs"
    )

    imageFiles = [
        f
        for f in os.listdir(sessionImageFolder)
        if os.path.isfile(os.path.join(sessionImageFolder, f))
    ]

    for fileName in imageFiles:
        analysisDir = os.path.join(sessionOutputFolder, fileName + "-analysis")

        if not os.path.isdir(analysisDir):
            os.mkdir(analysisDir)

            imageSrc = os.path.join(sessionImageFolder, fileName)
            imageDest = os.path.join(
                sessionOutputFolder, fileName + "-analysis", fileName
            )

            os.link(imageSrc, imageDest)


def update_session_status(id, status):
    sessionFolder = os.path.join(
        Config.config().get(section="API", option="StorageFolder"), id
    )

    with open(os.path.join(sessionFolder, "state.json"), "w+") as json_file:
        if os.stat(os.path.join(sessionFolder, "state.json")).st_size == 0:
            data = {}
        else:
            data = json.loads(json_file)

        data["status"] = status

        json_file.write(json.dumps(data))


def check_session_exists(id):
    session_folder = os.path.join(
        Config.config().get(section="API", option="StorageFolder"), id
    )

    state_file = os.path.join(session_folder, "state.json")

    if not os.path.isdir(session_folder) or not os.path.exists(state_file):
        return False
    else:
        return True
