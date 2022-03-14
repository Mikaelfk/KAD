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
        tags = ['Xmp', 'xmp']
        metadata = {}
        get_xmp_metadata(tags, result_data, metadata)

    img.modify_xmp(metadata)


def get_xmp_metadata(tags, result_data, metadata: dict):
    """A recursive function which adds all data to their own xmp tags

    Args:
        tags (list[str]): a list of the current xmp tags
        result_data (dict): the value of the current tags
        metadata (dict): the full xmp data which is to be added to the image
    """
    for key in result_data:
        # Appends the current key as a tag
        tags.append(key)
        value = result_data.get(key)

        if type(value) == dict:
            get_xmp_metadata(tags, value, metadata)
        else:
            metadata.update({'.'.join(tags): value})
        # Deletes the last tag from the list
        del tags[-1]
