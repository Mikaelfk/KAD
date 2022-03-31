"""Testing for file helpers
"""
import os

from werkzeug.datastructures import FileStorage
from kad.utils.file_helpers import is_file_empty


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def test_is_file_empty():
    """Postive test for is_file_empty method"""
    file = None
    with open(
        os.path.join(THIS_DIR, "test_pictures/test_image.jpg"), "rb"
    ) as file_read:
        file = FileStorage(file_read)
        assert not is_file_empty(file)


def test_is_file_empty_negative():
    """Negative test for is_file_empty method"""
    file = FileStorage()
    assert is_file_empty(file)
