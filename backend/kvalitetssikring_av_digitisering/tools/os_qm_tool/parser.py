import os


def result_parser(url):
    # Variables
    section_divider = "***********************************************************************"
    new_section = False
    section_name = ''
    section_content = ''

    # Read file
    with open(url) as f:
        lines = f.readlines()

    # Parse every line
    for line in lines:
        # find new section
        if line.__contains__(section_divider):
            # handle section content
            match section_name.lower():
                case "delta e": check_delta_e(section_content)
                case "noise": check_noise(section_content)
                case "oecf": check_oecf(section_content)
                case "mtf": check_mtf(section_content)
                case "homogeneity": check_homogeneity(section_content)
                case "geometry": check_geometry(section_content)
            # New section
            new_section = True
            section_content = ''
            continue

        # set section name
        if new_section:
            new_section = False
            section_name = line.replace(' check', '').strip()
            continue

        # get section content
        section_content += line


def check_delta_e(lines):
    print(lines)


def check_noise(lines):
    print(lines)


def check_oecf(lines):
    print(lines)


def check_mtf(lines):
    print(lines)


def check_homogeneity(lines):
    print(lines)


def check_geometry(lines):
    print(lines)


# Temp to test out parser
result_parser(r"C:\Users\Martin Holtmon\Documents\OSQMTOOL\runs\UTT\UTT_protokoll_summary.txt")
