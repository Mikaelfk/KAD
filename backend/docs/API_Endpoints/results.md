# /api/results/{:session_id}

Endpoint that gives complete results of current results of a session.


## Request

Method: GET


## Response

=== "200"
    OK
    ``` json linenums="1" title="JSON"
    {
        STRING: {
            CHAR: {
                "completed": BOOL,
                "results": {
                    "passed": BOOL,
                    STRING: {
                        ...
                    }
                    ...
                }
            },
            "image_tag": STRING,
            "overall_score": CHAR
        },
	    ...
    }
    ```

=== "404"
    Not found
    ``` json linenums="1" title="JSON"
    {
        "error": STRING
    }
    ```


## Sample Response

=== "200"
    OK
    ``` json linenums="1" title="JSON"
    {
        "UTT.tif": {
            "C": {
                "completed": true,
                "results": {
                    "passed": true,
                    "TonalReproduction": {
                        "Delta_C": "succeeded",
                        "Delta_E": "succeeded",
                        "Lab_L": "succeeded",
                        "Max_Gain_Modulation_L": "succeeded",
                        "Min_Gain_Modulation_L": "succeeded"
                    },
                    "Resolution": {
                        "MTF10": "succeeded",
                        "MTF50": "succeeded",
                        "Max_Misregistration": "succeeded",
                        "Max_Modulation": "succeeded",
                        "Min_Sampling_Efficiency": "succeeded",
                        "Obt_Sampling_Rate": "succeeded"
                    },
                    "Color": {
                        "Max_Delta_C": "succeeded",
                        "Max_Delta_E": "succeeded",
                        "Max_Delta_H": "succeeded",
                        "Max_Delta_L": "succeeded",
                        "Mean_Delta_C": "succeeded",
                        "Mean_Delta_E": "succeeded",
                        "Mean_Delta_H": "succeeded",
                        "Mean_Delta_L": "succeeded"
                    },
                    "Shading": {
                        "Max_Delta_Gray": "succeeded",
                        "Max_Delta_White": "succeeded"
                    },
                    "Distortion": {
                        "Max_Distortion": "succeeded"
                    },
                    "Lines": {
                        "Max_Out_Black": "succeeded",
                        "Max_Out_Gray": "succeeded",
                        "Max_Out_White": "succeeded"
                    },
                    "Noise": {
                        "Visual_Noise": "succeeded"
                    }
                }
            },
            "B": {
                "completed": true,
                "results": {
                    "passed": true,
                    "TonalReproduction": {
                        "Delta_C": "succeeded",
                        "Delta_E": "succeeded",
                        "Lab_L": "succeeded",
                        "Max_Gain_Modulation_L": "succeeded",
                        "Min_Gain_Modulation_L": "succeeded"
                    },
                    "Resolution": {
                        "MTF10": "succeeded",
                        "MTF50": "succeeded",
                        "Max_Misregistration": "succeeded",
                        "Max_Modulation": "succeeded",
                        "Min_Sampling_Efficiency": "succeeded",
                        "Obt_Sampling_Rate": "succeeded"
                    },
                    "Color": {
                        "Max_Delta_C": "succeeded",
                        "Max_Delta_E": "succeeded",
                        "Max_Delta_H": "succeeded",
                        "Max_Delta_L": "succeeded",
                        "Mean_Delta_C": "succeeded",
                        "Mean_Delta_E": "succeeded",
                        "Mean_Delta_H": "succeeded",
                        "Mean_Delta_L": "succeeded"
                    },
                    "Shading": {
                        "Max_Delta_Gray": "succeeded",
                        "Max_Delta_White": "succeeded"
                    },
                    "Distortion": {
                        "Max_Distortion": "succeeded"
                    },
                    "Lines": {
                        "Max_Out_Black": "succeeded",
                        "Max_Out_Gray": "succeeded",
                        "Max_Out_White": "succeeded"
                    },
                    "Noise": {
                        "Visual_Noise": "succeeded"
                    }
                }
            },
            "A": {
                "completed": true,
                "results": {
                    "passed": true,
                    "TonalReproduction": {
                        "Delta_C": "succeeded",
                        "Delta_E": "succeeded",
                        "Lab_L": "succeeded",
                        "Max_Gain_Modulation_L": "succeeded",
                        "Min_Gain_Modulation_L": "succeeded"
                    },
                    "Resolution": {
                        "MTF10": "succeeded",
                        "MTF50": "succeeded",
                        "Max_Misregistration": "succeeded",
                        "Max_Modulation": "succeeded",
                        "Min_Sampling_Efficiency": "succeeded",
                        "Obt_Sampling_Rate": "succeeded"
                    },
                    "Color": {
                        "Max_Delta_C": "succeeded",
                        "Max_Delta_E": "succeeded",
                        "Max_Delta_H": "succeeded",
                        "Max_Delta_L": "succeeded",
                        "Mean_Delta_C": "succeeded",
                        "Mean_Delta_E": "succeeded",
                        "Mean_Delta_H": "succeeded",
                        "Mean_Delta_L": "succeeded"
                    },
                    "Shading": {
                        "Max_Delta_Gray": "succeeded",
                        "Max_Delta_White": "succeeded"
                    },
                    "Distortion": {
                        "Max_Distortion": "succeeded"
                    },
                    "Lines": {
                        "Max_Out_Black": "succeeded",
                        "Max_Out_Gray": "succeeded",
                        "Max_Out_White": "succeeded"
                    },
                    "Noise": {
                        "Visual_Noise": "succeeded"
                    }
                }
            },
            "image_tag": "before_target",
            "overall_score": "A"
        },
        "e86a-UTT.tif": {
            "C": {
                "completed": true,
                "results": {
                    "passed": true,
                    "TonalReproduction": {
                        "Delta_C": "succeeded",
                        "Delta_E": "succeeded",
                        "Lab_L": "succeeded",
                        "Max_Gain_Modulation_L": "succeeded",
                        "Min_Gain_Modulation_L": "succeeded"
                    },
                    "Resolution": {
                        "MTF10": "succeeded",
                        "MTF50": "succeeded",
                        "Max_Misregistration": "succeeded",
                        "Max_Modulation": "succeeded",
                        "Min_Sampling_Efficiency": "succeeded",
                        "Obt_Sampling_Rate": "succeeded"
                    },
                    "Color": {
                        "Max_Delta_C": "succeeded",
                        "Max_Delta_E": "succeeded",
                        "Max_Delta_H": "succeeded",
                        "Max_Delta_L": "succeeded",
                        "Mean_Delta_C": "succeeded",
                        "Mean_Delta_E": "succeeded",
                        "Mean_Delta_H": "succeeded",
                        "Mean_Delta_L": "succeeded"
                    },
                    "Shading": {
                        "Max_Delta_Gray": "succeeded",
                        "Max_Delta_White": "succeeded"
                    },
                    "Distortion": {
                        "Max_Distortion": "succeeded"
                    },
                    "Lines": {
                        "Max_Out_Black": "succeeded",
                        "Max_Out_Gray": "succeeded",
                        "Max_Out_White": "succeeded"
                    },
                    "Noise": {
                        "Visual_Noise": "succeeded"
                    }
                }
            },
            "B": {
                "completed": true,
                "results": {
                    "passed": true,
                    "TonalReproduction": {
                        "Delta_C": "succeeded",
                        "Delta_E": "succeeded",
                        "Lab_L": "succeeded",
                        "Max_Gain_Modulation_L": "succeeded",
                        "Min_Gain_Modulation_L": "succeeded"
                    },
                    "Resolution": {
                        "MTF10": "succeeded",
                        "MTF50": "succeeded",
                        "Max_Misregistration": "succeeded",
                        "Max_Modulation": "succeeded",
                        "Min_Sampling_Efficiency": "succeeded",
                        "Obt_Sampling_Rate": "succeeded"
                    },
                    "Color": {
                        "Max_Delta_C": "succeeded",
                        "Max_Delta_E": "succeeded",
                        "Max_Delta_H": "succeeded",
                        "Max_Delta_L": "succeeded",
                        "Mean_Delta_C": "succeeded",
                        "Mean_Delta_E": "succeeded",
                        "Mean_Delta_H": "succeeded",
                        "Mean_Delta_L": "succeeded"
                    },
                    "Shading": {
                        "Max_Delta_Gray": "succeeded",
                        "Max_Delta_White": "succeeded"
                    },
                    "Distortion": {
                        "Max_Distortion": "succeeded"
                    },
                    "Lines": {
                        "Max_Out_Black": "succeeded",
                        "Max_Out_Gray": "succeeded",
                        "Max_Out_White": "succeeded"
                    },
                    "Noise": {
                        "Visual_Noise": "succeeded"
                    }
                }
            },
            "A": {
                "completed": true,
                "results": {
                    "passed": true,
                    "TonalReproduction": {
                        "Delta_C": "succeeded",
                        "Delta_E": "succeeded",
                        "Lab_L": "succeeded",
                        "Max_Gain_Modulation_L": "succeeded",
                        "Min_Gain_Modulation_L": "succeeded"
                    },
                    "Resolution": {
                        "MTF10": "succeeded",
                        "MTF50": "succeeded",
                        "Max_Misregistration": "succeeded",
                        "Max_Modulation": "succeeded",
                        "Min_Sampling_Efficiency": "succeeded",
                        "Obt_Sampling_Rate": "succeeded"
                    },
                    "Color": {
                        "Max_Delta_C": "succeeded",
                        "Max_Delta_E": "succeeded",
                        "Max_Delta_H": "succeeded",
                        "Max_Delta_L": "succeeded",
                        "Mean_Delta_C": "succeeded",
                        "Mean_Delta_E": "succeeded",
                        "Mean_Delta_H": "succeeded",
                        "Mean_Delta_L": "succeeded"
                    },
                    "Shading": {
                        "Max_Delta_Gray": "succeeded",
                        "Max_Delta_White": "succeeded"
                    },
                    "Distortion": {
                        "Max_Distortion": "succeeded"
                    },
                    "Lines": {
                        "Max_Out_Black": "succeeded",
                        "Max_Out_Gray": "succeeded",
                        "Max_Out_White": "succeeded"
                    },
                    "Noise": {
                        "Visual_Noise": "succeeded"
                    }
                }
            },
            "image_tag": "after_target",
            "overall_score": "A"
	    }
    }
    ```

=== "404"
    Not found
    ``` json linenums="1" title="JSON"
    {
	    "error": "session does not exist"
    }
    ```