import subprocess
import os

from kvalitetssikring_av_digitisering.config import Config


def run_analysis(image_file_path: str, specification_level: str):

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
