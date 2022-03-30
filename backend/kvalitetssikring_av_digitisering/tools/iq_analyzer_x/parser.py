"""Parser for IQ-Analyzer X
"""
import xml.etree.ElementTree as ET


def result_summary_parser(uri):
    """Parses IQ-Analyzer X analysis result XML file

    Args:
        uri (str): Path to protokoll summary

    Returns:
        dict: Overview results of analysis
    """
    # fix xml
    fixed_xml = fix_xml(uri)

    # Parse XML to find overview
    root = ET.fromstring(fixed_xml)
    overview_groups = root.findall("./Group/Image/Curves/UTT/Overview/*")
    if len(overview_groups) == 0:
        return {"passed": False}

    # Get results
    results = {}
    results.update({"passed": True})
    overall_score = True
    for group in overview_groups:
        children = group.findall("./*")

        children_states = {}
        for child in children:
            children_states.update({child.text: child.attrib.get("State")})
            if child.attrib.get("State") == "failed":
                overall_score = False
        # Update
        results.update({group.attrib.get("Type"): children_states})
    results.update({"passed": overall_score})

    return results


def fix_xml(uri):
    """Replace invalid FXML tag analysis result

    Args:
        uri (str): path to analysis

    Returns:
        str: xml result as a string
    """
    # Import data
    with open(uri, "r", encoding="UTF-8") as file:
        data = file.read().replace("\n", "")

    # Fix data
    data = data.replace("<Maximum delta L>", '<Maximum Type="delta L">')
    data = data.replace("</Maximum delta L>", "</Maximum>")

    return data
