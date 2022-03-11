import subprocess
import os

from kvalitetssikring_av_digitisering.config import Config
from kvalitetssikring_av_digitisering.session_manager import update_session_status


def run_analysis(image_file_path: str, specification_level: str):
    """Runs analysis on one image of given specification level

    Args:
        image_file_path (str): The path to the file which should be analyzed
        specification_level (str): Specification ISO level the image should be tested against

    Returns:
        bool: true if analysis passed, false otherwise
    """
    if specification_level not in ["A", "B", "C"]:
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
    image_file = os.path.normpath("{}".format(image_file_path))
    specification = "--specification='1'".format(1)

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
    )

    return True


def run_analyses(before_target_path: str, after_target_path: str, session_id: str):
    """Runs analysis using all three ISO levels on both before and after target

    Args:
        before_target_path (str): The target which is scanned at the start of an image batch
        after_target_path (str): The target which is scanend at the end of an image batch
        session_id (str): The session id of the current session so the session status can be updated.
    """
    scores = ["C", "B", "A"] 

    i = 0
    while(i < len(scores) and run_analysis(before_target_path ,scores[i]) and run_analysis(after_target_path, scores[i])):
        i += 1
    update_session_status(session_id, "Finished") 
