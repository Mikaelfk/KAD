from array import array
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
        result_data = data[name]
        key = ['Xmp', 'xmp']
        metadata = {}
        get_xmp_metadata(key, result_data, metadata)

    img.modify_xmp(metadata)


def get_xmp_metadata(key, result_data, metadata: dict):
    for v in result_data:
        key.append(v)
        if type(result_data.get(v)) == dict:
            get_xmp_metadata(key, result_data.get(v), metadata)
        else:
            metadata.update({'.'.join(key): result_data.get(v)})
            del key[-1]
