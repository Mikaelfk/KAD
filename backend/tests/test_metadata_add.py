import json
import os
import pyexiv2
from kvalitetssikring_av_digitisering.metadata_add import add_metadata_to_file

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def test_add_metadata_to_file():
    """Tests adding metadata to an image
    """
    test_file_path = os.path.join(
        THIS_DIR, "test_pictures", "test_metadata.jpg")

    img = pyexiv2.Image(test_file_path)
    img.clear_xmp()
    add_metadata_to_file(test_file_path, os.path.join(
        THIS_DIR, "test_data", 'test_results.json')
    )
    with pyexiv2.Image(test_file_path) as img:
        xmp_data = img.read_xmp()

    assert xmp_data == {'Xmp.xmp.test_metadata.jpg': "target_order before_target, B {'TonalReproduction': {'Delta_C': 'failed', 'Delta_E': 'succeeded', 'Lab_L': 'failed', 'Max_Gain_Modulation_L': 'failed', 'Min_Gain_Modulation_L': 'failed'}, 'Resolution': {'MTF10': 'succeeded', 'MTF50': 'succeeded', 'Max_Misregistration': 'succeeded', 'Max_Modulation': 'succeeded', 'Min_Sampling_Efficiency': 'succeeded', 'Obt_Sampling_Rate': 'succeeded'}, 'Color': {'Max_Delta_C': 'succeeded', 'Max_Delta_E': 'failed', 'Max_Delta_H': 'succeeded', 'Max_Delta_L': 'succeeded', 'Mean_Delta_C': 'succeeded', 'Mean_Delta_E': 'failed', 'Mean_Delta_H': 'succeeded', 'Mean_Delta_L': 'succeeded'}, 'Shading': {'Max_Delta_Gray': 'succeeded', 'Max_Delta_White': 'succeeded'}, 'Distortion': {'Max_Distortion': 'succeeded'}, 'Lines': {'Max_Out_Black': 'succeeded', 'Max_Out_Gray': 'succeeded', 'Max_Out_White': 'succeeded'}, 'Noise': {'Visual_Noise': 'succeeded'}}"}
