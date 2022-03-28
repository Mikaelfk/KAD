"""tests for image_zipper module
"""
import os.path

from kvalitetssikring_av_digitisering.utils.image_zipper import (
    zip_all_images_in_session,
)
from kvalitetssikring_av_digitisering.utils.path_helpers import get_session_dir
from kvalitetssikring_av_digitisering.utils.session_manager import create_session


def test_zip_all_images_in_session():
    """test for zip_all_images_in_session method"""
    session_id = create_session()

    zip_all_images_in_session(session_id)
    assert os.path.isfile(os.path.join(get_session_dir(session_id), "images.zip"))
