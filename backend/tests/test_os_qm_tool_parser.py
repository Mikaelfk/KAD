"""Testing OS QM Tool parser
"""
import os

from kvalitetssikring_av_digitisering.tools.os_qm_tool.parser import Check, Results
from kvalitetssikring_av_digitisering.tools.os_qm_tool.parser import (
    result_summary_parser as parser,
)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def test_parsing_utt():
    """Testing parser for OS QM Tool summary of UTT"""

    # Known values
    results = {
        "passed": True,
        "delta_e": {
            "result": True,
            "limits": {"max": "25.00", "mean": "12.00"},
            "values": {"max": "14.99", "min": "1.26", "mean": "5.33"},
        },
        "noise": {
            "result": True,
            "limits": {},
            "values": {
                "l* upperhorizontal": "0.92",
                "l* rightvertical": "0.91",
                "l* lowerhorizontal": "1.05",
                "l* leftvertical": "0.90",
            },
        },
        "oecf": {
            "result": True,
            "limits": {},
            "values": {
                "upperhorizontal": "41.84",
                "rightvertical": "41.41",
                "lowerhorizontal": "41.56",
                "leftvertical": "41.83",
            },
        },
        "mtf": {
            "result": True,
            "limits": {"minimum": "4.00 cycles/mm"},
            "values": {"mean": "7.59 cycles/mm"},
        },
        "homogeneity": {
            "result": True,
            "limits": {},
            "values": {
                "minimum mean": "229.41",
                "maximum mean": "235.74",
                "inhomogeneity": "6.33",
            },
        },
        "geometry": {
            "result": True,
            "limits": {"maximum": "3.00 %"},
            "values": {
                "horizontal": "300.22,",
                "vertical": "299.34",
                "deviation horizontal/vertical:": "0.29 %",
            },
        },
    }

    # Test
    path = os.path.join(THIS_DIR, "test_data", "test_utt_protokoll_summary.txt")
    data = parser(path)
    assert results == data
