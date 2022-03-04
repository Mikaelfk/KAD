import os
from unicodedata import name
from dataclasses import dataclass, fields
from warnings import catch_warnings


@dataclass
class Check:
    result: bool

    def reset(self):
        self.result = None


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
            # getattr will throw attributeError exception if named attribute is not found and default is not defined
            try:
                print(field.name, getattr(Results, field.name))
            except:
                print(field.name, "unknown")


def result_parser(url):
    data = Results
    section = Check(None)

    # Variables
    section_divider = "***********************************************************************"
    in_section = False
    section_name = ''

    # Read file
    with open(url) as f:
        lines = f.readlines()

    # Parse every line
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
            continue

        # set section name
        if section_name == '':
            section_name = line.replace(' check', '').strip()

        # handle section content
        if in_section and line.strip():
            line = line.lower().strip()

            # Get Result
            if line.startswith("result"):
                arr = line.split()
                if arr[1] == 'passed':
                    section.result = True

    # Print data
    data.print()


# Temp to test out parser
result_parser(r"C:\Users\Martin Holtmon\Documents\OSQMTOOL\runs\GTDevice\GTDevice_protokoll_summary.txt")
