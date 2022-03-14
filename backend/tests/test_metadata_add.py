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

    assert xmp_data == {'Xmp.xmp.target_order': 'before_target', 'Xmp.xmp.B.TonalReproduction.Delta_C': 'failed', 'Xmp.xmp.B.TonalReproduction.Delta_E': 'succeeded', 'Xmp.xmp.B.TonalReproduction.Lab_L': 'failed', 'Xmp.xmp.B.TonalReproduction.Max_Gain_Modulation_L': 'failed', 'Xmp.xmp.B.TonalReproduction.Min_Gain_Modulation_L': 'failed', 'Xmp.xmp.B.Resolution.MTF10': 'succeeded', 'Xmp.xmp.B.Resolution.MTF50': 'succeeded', 'Xmp.xmp.B.Resolution.Max_Misregistration': 'succeeded', 'Xmp.xmp.B.Resolution.Max_Modulation': 'succeeded', 'Xmp.xmp.B.Resolution.Min_Sampling_Efficiency': 'succeeded', 'Xmp.xmp.B.Resolution.Obt_Sampling_Rate': 'succeeded',
                        'Xmp.xmp.B.Color.Max_Delta_C': 'succeeded', 'Xmp.xmp.B.Color.Max_Delta_E': 'failed', 'Xmp.xmp.B.Color.Max_Delta_H': 'succeeded', 'Xmp.xmp.B.Color.Max_Delta_L': 'succeeded', 'Xmp.xmp.B.Color.Mean_Delta_C': 'succeeded', 'Xmp.xmp.B.Color.Mean_Delta_E': 'failed', 'Xmp.xmp.B.Color.Mean_Delta_H': 'succeeded', 'Xmp.xmp.B.Color.Mean_Delta_L': 'succeeded', 'Xmp.xmp.B.Shading.Max_Delta_Gray': 'succeeded', 'Xmp.xmp.B.Shading.Max_Delta_White': 'succeeded', 'Xmp.xmp.B.Distortion.Max_Distortion': 'succeeded', 'Xmp.xmp.B.Lines.Max_Out_Black': 'succeeded', 'Xmp.xmp.B.Lines.Max_Out_Gray': 'succeeded', 'Xmp.xmp.B.Lines.Max_Out_White': 'succeeded', 'Xmp.xmp.B.Noise.Visual_Noise': 'succeeded'}
