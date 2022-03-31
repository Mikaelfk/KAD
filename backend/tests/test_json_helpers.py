"""
"""
import os
import shutil
from kad.utils.json_helpers import (
    json_get_best_passing_iso_score,
    json_iqx_set_image_tag,
    json_set_overall_score,
    read_from_json_file,
    write_to_json_file,
    json_iqx_add_result,
    json_iqx_set_analysis_failed,
)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_JSON_FILE = os.path.join(THIS_DIR, "test_data", "test_results.json")
FILE_NAME = os.path.basename(os.path.normpath(TEST_JSON_FILE))

TEST_AGAINST_DATA = {
    "test_metadata.jpg": {
        "target_order": "before_target",
        "B": {
            "completed": True,
            "results": {
                "passed": True,
                "TonalReproduction": {
                    "Delta_C": "failed",
                    "Delta_E": "succeeded",
                    "Lab_L": "failed",
                    "Max_Gain_Modulation_L": "failed",
                    "Min_Gain_Modulation_L": "failed",
                },
                "Resolution": {
                    "MTF10": "succeeded",
                    "MTF50": "succeeded",
                    "Max_Misregistration": "succeeded",
                    "Max_Modulation": "succeeded",
                    "Min_Sampling_Efficiency": "succeeded",
                    "Obt_Sampling_Rate": "succeeded",
                },
                "Color": {
                    "Max_Delta_C": "succeeded",
                    "Max_Delta_E": "failed",
                    "Max_Delta_H": "succeeded",
                    "Max_Delta_L": "succeeded",
                    "Mean_Delta_C": "succeeded",
                    "Mean_Delta_E": "failed",
                    "Mean_Delta_H": "succeeded",
                    "Mean_Delta_L": "succeeded",
                },
                "Shading": {
                    "Max_Delta_Gray": "succeeded",
                    "Max_Delta_White": "succeeded",
                },
                "Distortion": {"Max_Distortion": "succeeded"},
                "Lines": {
                    "Max_Out_Black": "succeeded",
                    "Max_Out_Gray": "succeeded",
                    "Max_Out_White": "succeeded",
                },
                "Noise": {"Visual_Noise": "succeeded"},
            },
        },
    }
}


def test_read_from_json_file():
    """test for read_from_json_file method"""
    data = read_from_json_file(TEST_JSON_FILE)
    assert data == TEST_AGAINST_DATA


def test_write_to_json_file():
    """test for write_to_json_file method"""

    src = TEST_JSON_FILE
    dst = os.path.join(THIS_DIR, "test_data", "test_results_writeable.json")
    shutil.copyfile(src, dst)

    write_to_json_file(dst, {"written_data": "testing"})

    data = read_from_json_file(dst)
    os.remove(dst)
    assert data == {"written_data": "testing"}


def test_json_iqx_add_results():
    """test for json_iqx_add_results method"""
    data = read_from_json_file(TEST_JSON_FILE)
    data = json_iqx_add_result(data, FILE_NAME, "A", {"test_key": "test_value"})
    test_data = TEST_AGAINST_DATA
    test_data[FILE_NAME] = {
        "A": {"completed": True, "results": {"test_key": "test_value"}}
    }
    assert data == test_data


def test_json_iqx_set_analysis_failed():
    """test for json_iqx_set_analysis_failed method"""
    data = read_from_json_file(TEST_JSON_FILE)
    data = json_iqx_set_analysis_failed(data, FILE_NAME, "A")
    test_data = TEST_AGAINST_DATA
    test_data[FILE_NAME] = {"A": {"completed": False}}
    assert data == test_data


def test_json_iqx_set_image_tag():
    """test for json_iqx_set_image_tag method"""
    data = read_from_json_file(TEST_JSON_FILE)
    data = json_iqx_set_image_tag(data, FILE_NAME, "before_target")
    test_data = TEST_AGAINST_DATA
    test_data[FILE_NAME] = {"image_tag": "before_target"}
    assert data == test_data


def test_json_iqx_set_overall_score():
    """test for json_iqx_set_overall_score method"""
    data = read_from_json_file(TEST_JSON_FILE)
    data = json_set_overall_score(data, FILE_NAME, "A")
    test_data = TEST_AGAINST_DATA
    test_data[FILE_NAME] = {"overall_score": "A"}
    assert data == test_data


def test_json_get_best_passing_iso_score():
    """test for json_get_best_passing_iso_score method"""
    data = read_from_json_file(TEST_JSON_FILE)
    score = json_get_best_passing_iso_score(data, "test_metadata.jpg")
    assert score == "B"
