import os
from sys import flags
from tabnanny import check
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
            # Update data with section/results
            if section_name in data.__match_args__:
                data.__setattr__(section_name, section) 

            # New section
            in_section = True
            section_name = ''
            section = Check()
            continue

        # set section name
        if section_name == '':
            section_name = line.replace(' check', '').strip().lower().replace(' ', '_')

        # handle section content
        if in_section and line.strip():
            line = line.lower().strip()
            section_handler(section, section_name, line)           


    # Print data
    print(data)

def section_handler(section: Check, section_name, line):
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
    
    # Spesific section filters
    match section_name:
        case "delta_e": check_delta_e(section, line)
        case "noise": check_noise(section, line)
        case "oecf": check_oecf(section, line)
        case "mtf": check_mtf(section, line)
        case "homogeneity": check_homogeneity(section, line)
        case "geometry": check_geometry(section, line)

def check_delta_e(section: Check, line):
    # Get limits (delta E)
    # Limits
        # Max Delta E: 25.00
        # Mean Delta E: 12.00
    if line.startswith("max delta e"):
        arr = line.split()
        section.limits.update({'max': arr[3]})
    if line.startswith("mean delta e"):
        arr = line.split()
        section.limits.update({'mean': arr[3]})
    return section

def check_noise(section: Check, line):
    return section

def check_oecf(section: Check, line):
    return section

def check_mtf(section: Check, line):
    return section

def check_homogeneity(section: Check, line):
    return section

def check_geometry(section: Check, line):
    return section


# Temp to test out parser
result_parser(
    r"C:\Users\Martin Holtmon\Documents\OSQMTOOL\runs\GTDevice\GTDevice_protokoll_summary.txt")
