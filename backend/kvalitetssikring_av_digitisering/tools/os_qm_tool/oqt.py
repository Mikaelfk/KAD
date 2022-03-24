import os
import subprocess

from kvalitetssikring_av_digitisering.config import Config

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def run_analysis(
    image_file: str, target_name: str, output_file: str, specification_level: str
):

    if specification_level not in ["A", "B", "C"]:
        return False

    parameter_folder = os.path.join(THIS_DIR, "resources", "parameter_files")
    match target_name:
        case "UTT" | "TE263" | "GTObject" | "GTDevice":
            parameter_file = os.path.join(
                parameter_folder, f"{target_name}_{specification_level}.qmp"
            )
        case _:
            return False

    print(parameter_file)

    print(image_file)

    print(output_file)

    oqt_executable = os.path.join(
        Config.config().get(section="OS QM-Tool", option="InstallPath"),
        "QMTool.exe",
    )
    try:
        # order of arguments somewhat arbitrary, but chose same as example in manual just in case
        subprocess.run(
            [
                oqt_executable,
                image_file,
                parameter_file,
                output_file,
            ],
            timeout=int(
                Config.config().get(section="OS QM-Tool", option="SessionTimeout")
            ),
            check=True,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False

    return True
