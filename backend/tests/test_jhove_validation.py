import os
import configparser

from kvalitetssikring_av_digitisering.file_validation import jhove_validation

config = configparser.ConfigParser()
config.read("./config")

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def test_jhove_validation_good():
    """Testing JHOVE validation on good image
    """

    image_good = THIS_DIR + "/test_pictures/test_image.jpg"
    output = jhove_validation(image_good)
    assert output[1] == True


def test_jhove_validation_bad():
    """Testing JHOVE validation on bad image
    """

    image_bad = THIS_DIR + "/test_pictures/test_image-bad.jpg"
    output = jhove_validation(image_bad)
    assert output[1] == False
