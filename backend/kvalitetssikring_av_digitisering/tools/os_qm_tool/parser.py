"""Parser for the summary output from OS QM Tool
"""
import typing
from dataclasses import asdict, dataclass, field, fields


@dataclass
class Check:
    """Dataclass for each check done by OS QM Tool

    Arg:
        result (bool): if the check passed or failed
        limits (dict): A map of the limits for each check
        values (dict): A map of the values for each check

    Returns:
        dataclass: info about each check (section)
    """

    result: typing.Optional[bool] = None
    limits: dict = field(default_factory=dict)
    values: dict = field(default_factory=dict)


@dataclass
class Results:
    """Dataclass for the results extracted from the summary

    Arg:
        delta_e (dataclass): Information about the Delta E check
        noise (dataclass): Information about the Noise check
        oecf (dataclass): Information about the OECF check
        mtf (dataclass): Information about the MTF check
        homogeneity (dataclass): Information about the Homogeneity check
        geometry (dataclass): Information about the Geometry check

    Returns:
        dataclass: Data of the results
    """

    passed: typing.Optional[bool] = None
    delta_e: Check = Check()
    noise: Check = Check()
    oecf: Check = Check()
    mtf: Check = Check()
    homogeneity: Check = Check()
    geometry: Check = Check()


def result_summary_parser(url):
    """Parser for the summary output from OS QM Tool

    Args:
        url (str): Path to summary file

    Returns:
        dataclass: Structured results extracted from the summary output
    """

    # Variables
    data = Results()
    section = Check()
    section_divider = (
        "***********************************************************************"
    )
    in_section = False
    section_name = ""
    prev_line = str

    # Read file
    with open(url, encoding="UTF-8") as file:
        lines = file.readlines()

    # Makes a list of all the field names in the Results dataclass
    field_names = []
    for field_name in asdict(data):
        field_names.append(field_name)

    # Parse every line
    for line in lines:
        # find new section
        if line.__contains__(section_divider):
            # Update data with section/results
            if section_name in field_names:
                data.__setattr__(section_name, section)

            # New section
            in_section = True
            section_name = ""
            section = Check()
            continue

        # set section name
        if section_name == "":
            section_name = line.replace(" check", "").strip().lower().replace(" ", "_")

        # handle section content
        if in_section and line.strip():
            line = line.lower().strip()
            try:
                section_handler(section, section_name, line, prev_line)
            except Exception as exception:
                print("Error while parsing " + section_name + ": " + str(exception))

            # Store line
            prev_line = line

    # Return data
    set_overall_score(data)
    return data


def section_handler(section: Check, section_name, line, prev_line):
    """Handler for each section

    This function will parse every line from the summary result and forward it to the correct section handler.
    It will do general filtering before sending it into spesific filters for each check (section).

    Args:
        section (Check): The section we are currently parsing
        section_name (str): Name of the section
        line (str): The current line we are parsing
        prev_line (str): The previous line we were parsing
    """

    # General filters
    # Get Result
    if line.startswith("result"):
        arr = line.split()
        if arr[1] == "passed":
            section.result = True
        else:
            section.result = False

    # Limits (MTF + Geometry)
    if line.startswith("limits"):
        arr = line.split()
        if len(arr) > 1:
            section.limits.update({arr[1]: " ".join(arr[4:6])})

    # Spesific section filters
    match section_name:
        case "delta_e":
            check_delta_e(section, line)
        case "noise":
            check_noise(section, line)
        case "oecf":
            check_oecf(section, line, prev_line)
        case "mtf":
            check_mtf(section, line)
        case "homogeneity":
            check_homogeneity(section, line)
        case "geometry":
            check_geometry(section, line)
        case _:
            raise NotImplementedError("section does not exist")


def check_delta_e(section: Check, line):
    """Spesific filter for the Delta E check

    Args:
        section (Check): The section we are currently parsing
        line (str): The current line we are parsing
    """

    # Get limits (delta E)
    if line.startswith("max delta e"):
        arr = line.split()
        section.limits.update({"max": arr[3]})
    if line.startswith("mean delta e"):
        arr = line.split()
        section.limits.update({"mean": arr[3]})

    # Measured Values.
    if line.startswith("delta e -"):
        arr = line.split()
        section.values.update({arr[3].replace(".", ""): arr[8]})


def check_noise(section: Check, line):
    """Spesific filter for the noise check

    Args:
        section (Check): The section we are currently parsing
        line (str): The current line we are parsing
    """
    # Measured Values:
    if line.startswith("l*"):
        arr = line.split()
        section.values.update({" ".join(arr[0:2]): arr[4]})


def check_oecf(section: Check, line, prev_line):
    """Spesific filter for the OECF check

    Args:
        section (Check): The section we are currently parsing
        line (str): The current line we are parsing
        prev_line (str): The previous line we were parsing
    """
    # Measured Values
    if line.startswith("l:"):
        # Get location (UpperHorizontal etc..)
        location = prev_line.split()[0]
        arr = line.split()
        section.values.update({location: arr[1]})


def check_mtf(section: Check, line):
    """Spesific filter for the MTF check

    Args:
        section (Check): The section we are currently parsing
        line (str): The current line we are parsing
    """
    # Measured Values
    if line.startswith("mean"):
        arr = line.split()
        section.values.update({arr[0][:-1]: " ".join(arr[1:3])})


def check_homogeneity(section: Check, line):
    """Spesific filter for the homogeneity check

    Args:
        section (Check): The section we are currently parsing
        line (str): The current line we are parsing
    """
    # Measured Values
    if line.startswith("minimum mean:") or line.startswith("maximum mean:"):
        arr = line.split()
        section.values.update({" ".join(arr[0:2])[:-1]: arr[2]})
    if line.startswith("inhomogeneity:"):
        arr = line.split()
        section.values.update({arr[0][:-1]: arr[1]})


def check_geometry(section: Check, line):
    """Spesific filter for the geometry check

    Args:
        section (Check): The section we are currently parsing
        line (str): The current line we are parsing
    """
    # Measured Values
    if line.startswith("measured values"):
        arr = line.split()
        set_geometry_value(section, arr, "horizontal:")
        set_geometry_value(section, arr, "vertical:")
        set_geometry_value(section, arr, "deviation")


def set_geometry_value(section, arr, name):
    """Sets values for the geometry check

    Args:
        section (Check): The section we are currently parsing
        arr (str): The current line we are parsing as an array
        name (str): The value we are looking for in the array
    """

    try:
        i = arr.index(name)
        if name == "deviation":
            section.values.update(
                {" ".join(arr[i : i + 2]): " ".join(arr[i + 2 : i + 4])}
            )
        else:
            # Update
            section.values.update({arr[i][:-1]: arr[i + 1]})
    except ValueError:
        print("Did not find " + name + " value")


def set_overall_score(data: Results):
    """Set the overall score for the results

    If all sections passed, then the overall score passed.

    Args:
        data (Results): The results
    """
    score = True
    for data_field in fields(data):
        check = getattr(data, data_field.name)
        if isinstance(check, Check) and check.result is False:
            score = False
    data.passed = score
