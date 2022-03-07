import os
from sys import flags
from unicodedata import name
from dataclasses import dataclass, fields, field
from warnings import catch_warnings


@dataclass
class Check:
    result: bool = None
    limits: dict = field(default_factory=dict)
    values: dict = field(default_factory=dict)
    deviation: dict = field(default_factory=dict)


@dataclass
class Results:
    delta_e: dataclass = Check()
    noise: dataclass = Check()
    oecf: dataclass = Check()
    mtf: dataclass = Check()
    homogeneity: dataclass = Check()
    geometry: dataclass = Check()


def result_parser(url):
    # Variables
    section_divider = "***********************************************************************"
    in_section = False
    section_name = ''

    # Read file
    with open(url) as f:
        lines = f.readlines()

    # Parse every line
    data = Results()
    section = Check()
    for line in lines:
        # find new section
        if line.__contains__(section_divider):
            # Update data with results
            match section_name.lower():
                case "delta e": data.delta_e = section
                case "noise": data.noise = section
                case "oecf": data.oecf = section
                case "mtf": data.mtf = section
                case "homogeneity": data.homogeneity = section
                case "geometry": data.geometry = section

            # New section
            in_section = True
            section_name = ''
            section = Check()
            continue

        # set section name
        if section_name == '':
            section_name = line.replace(' check', '').strip()

        # handle section content
        if in_section and line.strip():
            line = line.lower().strip()

            ## General filters
            # Get Result
            if line.startswith("result"):
                arr = line.split()
                if arr[1] == 'passed':
                    section.result = True
                else:
                    section.result = False
            
            # Limits
            if line.startswith("limits"):
                arr = line.split()
                if len(arr) > 1:
                    key = ' '.join(arr[i] for i in [1,3])[:-1]
                    value = arr[4]
                    section.limits.update({key: value})
            

            # Delta E filter
            if section_name == 'Delta E':
                section.limits = check_delta_e(line, section.limits)
            


    # Print data
    print(data)


def check_delta_e(line, data):
    # Get limits (delta E)
    # Limits
    # Max Delta E: 25.00
    # Mean Delta E: 12.00
    if line.startswith("max delta e"):
        arr = line.split()
        data.update({'Max': arr[3]})
    if line.startswith("mean delta e"):
        arr = line.split()
        data.update({'Mean': arr[3]})
    return data

# Temp to test out parser
result_parser(
    r"C:\Users\Martin Holtmon\Documents\OSQMTOOL\runs\GTDevice\GTDevice_protokoll_summary.txt")
