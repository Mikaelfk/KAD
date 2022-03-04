import os
from unicodedata import name
from dataclasses import dataclass, fields
from warnings import catch_warnings

@dataclass
class Check:
    result: bool

@dataclass
class Results:
    delta_e: dataclass = Check(None)
    noise: dataclass = Check(None)
    oecf: dataclass = Check(None)
    mtf: dataclass = Check(None)
    homogeneity: dataclass = Check(None)
    geometry: dataclass = Check(None)

    @staticmethod
    def print():
        for field in fields(Results):
            try: 
                print(field.name, getattr(Results, field.name))
            except: 
                continue


def result_parser(url):
    data = Results

    # Variables
    section_divider = "***********************************************************************"
    section = False
    section_name = ''
    section_content = []

    # Read file
    with open(url) as f:
        lines = f.readlines()

    # Parse every line
    for line in lines:
        # find new section
        if line.__contains__(section_divider):
            # handle section content
            match section_name.lower():
                case "delta e": data.delta_e = check_section(section_content)
                case "noise": data.noise = check_section(section_content)
                case "oecf": data.oecf = check_section(section_content)
                case "mtf": data.mtf = check_section(section_content)
                case "homogeneity": data.homogeneity = check_section(section_content)
                case "geometry": data.geometry = check_section(section_content)
            # New section
            section = True
            section_name = ''
            section_content.clear()
            continue

        # set section name
        if section_name == '':
            section_name = line.replace(' check', '').strip()

        # get section content
        if section and line.strip():
            section_content.append(line)
    data.print()



def check_section(lines):
    result = False
    for line in lines:
        line = line.lower().strip()
        if line.startswith("result"):
            arr = line.split()
            if arr[1] == 'passed': result = True;
    
    return Check(result)


# Temp to test out parser
result_parser(
    r"C:\Users\Martin Holtmon\Documents\OSQMTOOL\runs\GTDevice\GTDevice_protokoll_summary.txt")
