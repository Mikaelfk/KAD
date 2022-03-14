import pyexiv2
import json
import os


def add_metadata_to_file(file_path, result_file):
    """Adds json result as metadata to a given file

    Args:
        file_path (str): Path to the image
        result_file (str): Path to the result json file
    """
    img = pyexiv2.Image(file_path)
    name = os.path.basename(os.path.normpath(file_path))
    with open(result_file, "r") as json_result:
        data = json.load(json_result)
        data['Xmp.xmp.'+name] = data[name]
        del data[name]

    img.modify_xmp(data)
