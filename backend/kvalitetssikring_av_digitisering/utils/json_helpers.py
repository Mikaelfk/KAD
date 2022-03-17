"""Module for simplifying json file management.

Contains methods needed for reading and updating data in json files.
"""

import json
import os
from collections import defaultdict


def read_from_json_file(path_to_json_file: str):
    """Method for opening a file and reading the json data in it.

    Args:
        path_to_json_file (str): path to the json file to read from

    Returns:
        dict: python data
    """

    with open(path_to_json_file, "a+", encoding="UTF-8") as json_file:
        json_file.seek(0)

        if os.path.getsize(path_to_json_file) > 0:
            return json.load(json_file)

        return {}


def write_to_json_file(path_to_json_file: str, json_data: dict | defaultdict):
    """Method for opening a file and writing json data to it.

    note: will overwrite existing data.

    Args:
        path_to_json_file (str): path to the json file to write to
    """

    with open(path_to_json_file, "w+", encoding="UTF-8") as json_file:
        json_file.write(json.dumps(dict(json_data)))


def json_iqx_add_result(
    json_data: dict, file_name: str, specification_level: str, results: dict
):
    """Method for adding a analysis result to iqx result json.

    Args:
        json_data (dict): json data to add results to
        file_name (str): name of file to add results to
        specification_level (str): specification level for analysis
        results (str): analysis results

    Returns:
        dict: updated json data
    """

    data = defaultdict(dict, json_data)
    data[file_name][specification_level]["completed"] = True
    data[file_name][specification_level][results] = results
    return dict(data)


def json_iqx_set_analysis_failed(
    json_data: dict, file_name: str, specification_level: str
):
    """Method for setting an iqx analysis result to failed.

    Args:
        json_data (dict): json data to add results to
        file_name (str): name of file to add results to
        specification_level (str): specification level for analysis

    Returns:
        dict: updated json data
    """

    data = defaultdict(dict, json_data)
    data[file_name][specification_level]["completed"] = False
    return dict(data)


def json_iqx_set_image_tag(json_data: dict, file_name: str, image_tag: str):
    """Method for setting a tag to image in iqx result json.

    Args:
        json_data (dict): json data to set tag in
        file_name (str): name of file set tag on
        image_tag (str): tag to add

    Returns:
        dict: updated json data
    """

    data = defaultdict(dict, json_data)
    data[file_name]["image_tag"] = image_tag
    return dict(data)


def json_iqx_set_overall_score(json_data: dict, overall_score: str):
    """Method for setting the overall score of a iqx analysis result.

    Args:
        json_data (dict): json data to set overall score in
        overall_score (str): overall score to set

    Returns:
        dict: updated json data
    """

    data = defaultdict(str, json_data)
    data["overall_score"] = overall_score
    return dict(data)
