import pytest
import os

from dotenv import load_dotenv

from kvalitetssikring_av_digitisering.file_validation import jhove_validation

load_dotenv()
jhove_path = os.getenv('JHOVE_PATH')
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def test_jhove_validation_good():
    image_good = THIS_DIR + "/test_pictures/test_image.jpg"
    output = jhove_validation(image_good, jhove_path) 
    assert output[1] == True

def test_jhove_validation_bad():
    image_bad = THIS_DIR + "/test_pictures/test_image-bad.jpg"
    output = jhove_validation(image_bad, jhove_path) 
    assert output[1] == False
