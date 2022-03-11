"""Testing IQ-Analyzer-X parser
"""
import os
from kvalitetssikring_av_digitisering.tools.iq_analyzer_x.parser import result_summary_parser as parser

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def test_result_summary_parser():
    """Test the parser against known data
    """
    test_data = {
        'TonalReproduction': {'Delta_C': 'failed', 'Delta_E': 'succeeded', 'Lab_L': 'failed', 'Max_Gain_Modulation_L': 'failed', 'Min_Gain_Modulation_L': 'failed'}, 
        'Resolution': {'MTF10': 'succeeded', 'MTF50': 'succeeded', 'Max_Misregistration': 'succeeded', 'Max_Modulation': 'succeeded', 'Min_Sampling_Efficiency': 'succeeded', 'Obt_Sampling_Rate': 'succeeded'}, 
        'Color': {'Max_Delta_C': 'succeeded', 'Max_Delta_E': 'failed', 'Max_Delta_H': 'succeeded', 'Max_Delta_L': 'succeeded', 'Mean_Delta_C': 'succeeded', 'Mean_Delta_E': 'failed', 'Mean_Delta_H': 'succeeded', 'Mean_Delta_L': 'succeeded'}, 
        'Shading': {'Max_Delta_Gray': 'succeeded', 'Max_Delta_White': 'succeeded'}, 
        'Distortion': {'Max_Distortion': 'succeeded'}, 
        'Lines': {'Max_Out_Black': 'succeeded', 'Max_Out_Gray': 'succeeded', 'Max_Out_White': 'succeeded'}, 
        'Noise': {'Visual_Noise': 'succeeded'}
        }

    file = os.path.join(THIS_DIR, "test_data", "test_analysis_result.xml")
    data = parser(file)
    assert data == test_data