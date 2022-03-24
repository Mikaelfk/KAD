"""Module for adding metadata to a file
"""
import json
import pyexiv2


def add_metadata_to_file(file_path, result_dict: dict):
    """Adds json result as metadata to a given file

    Args:
        file_path (str): Path to the image
        result_file (str): Path to the result json file
    """
    img = pyexiv2.Image(file_path)
    data = result_dict
    tags = ["Xmp", "xmp"]
    metadata = {}
    get_xmp_metadata(tags, data, metadata)
    img.modify_xmp(metadata)
    img.close()


def get_xmp_metadata(tags, result_data, metadata: dict):
    """A recursive function which adds all data to their own xmp tags

    Args:
        tags (list[str]): a list of the current xmp tags
        result_data (dict): the value of the current tags
        metadata (dict): the full xmp data which is to be added to the image
    """
    for key in result_data:
        # Appends the current key as a tag
        tags.append(
            key.replace(" ", "_").replace("*", "").replace("/", "").replace(":", "")
        )
        value = result_data.get(key)

        if type(value) == dict:
            get_xmp_metadata(tags, value, metadata)
        else:
            metadata.update({".".join(tags): value})
        # Deletes the last tag from the list
        del tags[-1]
