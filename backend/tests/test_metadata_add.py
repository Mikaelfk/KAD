"""Testing adding metadata to image
"""
import os

import pyexiv2
from kvalitetssikring_av_digitisering.utils.json_helpers import read_from_json_file
from kvalitetssikring_av_digitisering.utils.metadata_add import add_metadata_to_file

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def test_add_metadata_to_file():
    """Tests adding metadata to an image"""
    test_file_path = os.path.join(THIS_DIR, "test_pictures", "test_metadata.jpg")

    img = pyexiv2.Image(test_file_path)
    img.clear_xmp()
    data = read_from_json_file(os.path.join(THIS_DIR, "test_data", "test_results.json"))
    add_metadata_to_file(test_file_path, data)
    with pyexiv2.Image(test_file_path) as img:
        xmp_data = img.read_xmp()
    print(xmp_data)
    assert xmp_data == {
        "Xmp.xmp.test_metadata.jpg.target_order": "before_target",
        "Xmp.xmp.test_metadata.jpg.B.completed": "True",
        "Xmp.xmp.test_metadata.jpg.B.results.passed": "True",
        "Xmp.xmp.test_metadata.jpg.B.results.TonalReproduction.Delta_C": "failed",
        "Xmp.xmp.test_metadata.jpg.B.results.TonalReproduction.Delta_E": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.TonalReproduction.Lab_L": "failed",
        "Xmp.xmp.test_metadata.jpg.B.results.TonalReproduction.Max_Gain_Modulation_L": "failed",
        "Xmp.xmp.test_metadata.jpg.B.results.TonalReproduction.Min_Gain_Modulation_L": "failed",
        "Xmp.xmp.test_metadata.jpg.B.results.Resolution.MTF10": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Resolution.MTF50": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Resolution.Max_Misregistration": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Resolution.Max_Modulation": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Resolution.Min_Sampling_Efficiency": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Resolution.Obt_Sampling_Rate": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Color.Max_Delta_C": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Color.Max_Delta_E": "failed",
        "Xmp.xmp.test_metadata.jpg.B.results.Color.Max_Delta_H": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Color.Max_Delta_L": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Color.Mean_Delta_C": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Color.Mean_Delta_E": "failed",
        "Xmp.xmp.test_metadata.jpg.B.results.Color.Mean_Delta_H": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Color.Mean_Delta_L": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Shading.Max_Delta_Gray": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Shading.Max_Delta_White": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Distortion.Max_Distortion": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Lines.Max_Out_Black": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Lines.Max_Out_Gray": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Lines.Max_Out_White": "succeeded",
        "Xmp.xmp.test_metadata.jpg.B.results.Noise.Visual_Noise": "succeeded",
    }
