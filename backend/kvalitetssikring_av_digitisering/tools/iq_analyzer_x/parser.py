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

    # Parse XML to find overview
    tree = ET.parse(uri)
    root = tree.getroot()
    overview_groups = root.findall('./Group/Image/Curves/UTT/Overview/*')

    # Get results
    results = {}
    for group in overview_groups:
        children = group.findall('./*')

        children_states = {}
        for child in children:
            children_states.update({child.text: child.attrib.get('State')})

        # Update
        results.update({group.attrib.get('Type'): children_states})

    return results
