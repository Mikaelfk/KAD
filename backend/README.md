# KAD

- [Requirements](#requirements)
    - [Installation](#installation)
    - [Overview](#overview)
- [Usage](#usage)
    - [Image Quality Evaluation (IQE) Software](#image-quality-evaluation-iqe-software)
    - [Config](#config)
    - [Running](#running)
    - [Connect](#connect)
    - [Tests](#tests)
- [API Documentation](#api-documentation)
    - [Local viewing](#local-viewing)
- [Notes](#notes)
    - [IQES are dependent on their GUI](#iqes-are-dependent-on-their-gui)
    - [OS QM-Tool command line support](#os-qm-tool-command-line-support)
    - [OS QM-Tool parameter files](#os-qm-tool-parameter-files)
- [Troubleshooting](#troubleshooting)
    - [OS QM-Tool sometimes does not work on all images](#os-qm-tool-sometimes-does-not-work-on-all-images)

## Requirements

Known working Python version: `3.10`

### Installation

Using pip:
```
pip install -r requirements.txt
```

### Overview

Runtime requirements:
- [Flask](https://github.com/pallets/flask/)
    - For routing and serving API
- [Flask-cors](https://github.com/corydolphin/flask-cors)
    - For compatability when serving frontend on a domain and connecting to backend with just IP
- [pyexiv2](https://github.com/LeoHsiao1/pyexiv2)
    - For adding metadata to images

Test requirements:
- [pytest](https://github.com/pytest-dev/pytest)
    - For testing

API documentation requirements:
- [MkDocs](https://github.com/mkdocs/mkdocs/)
    - For generating documentation pages
- [Material for MkDocs](https://github.com/squidfunk/mkdocs-material)
    - For layout and visual style

## Usage

### Image Quality Evaluation (IQE) Software

This module currently supports two IQE software:
- [iQ-Analyzer-X](https://image-engineering.de/products/software/iq-analyzer-x/) by Image Engineering
    - Known working version: `V1.5.1`
    - Has a free version, but requires license to use in automated manner   
- [OS QM-Tool](https://www.zeutschel.de/en/software/qm-os/) by Zeutschel
    - Known working verision: `Version 1.0 Build 718`
    - No free version, requires license to use

### Config

The repo includes a [config file template](config.ini.template) that needs to be filled out with necessary information for the module to run. 

The module will look for the config file in the working directory. Most of the time this will be where it is executed from. 

### Running

To run this module, a simple [`run.py`](run.py) script has been included. This script simply calls the `start()` method in [`main.py`](kad/main.py), which will start the flask server and listen for incoming connections.

### Connect

To use the module, refer to the [API Documentation](#api-documentation) to see what requests to make.

### Tests
Tests can be be run by first installing the required dependecies, and then running pytest:
```
pip -r requirements.txt
pip -m pytest tests/
```

## API Documentation

The API documentation is made to be displayed with Mkdocs. All pages are contained within [`docs/`](docs/), and the configuration is found in [`mkdocs.yml`](mkdocs.yml)

A live version of the documentation can be found on [GitLab Pages](https://bachelor_group9_2022.gitlab.io/kvalitetssikring-av-digitisering/docs/)

### Local viewing 

It can be dynamically served with:
```
mkdocs serve
```

Or statically built with:
```
mkdocs build
```

## Notes

### IQES are dependent on their GUI
Both image quality evaluation softwares currently supported are dependent on their GUI. This means that when running the backend, the softwares will pop up and perform analysis in GUI when started by backend.

### OS QM-Tool command line support 
Running OS QM-Tool through command line is not documented or officially supported, therefore it could easily break in the future without any notice.

### OS QM-Tool parameter files
OS QM Tool parameter files are manually made from reference file and may have some human errors, although currently there aren't any known errors. 

## Troubleshooting 

### OS QM-Tool sometimes does not work on all images
For unknown reasons, sometimes OS QM-Tool returns exit code 2 and/or a C++ runtime error when attempting to analyze image. In our testing, this is a result of bad conversion from PNG to JPEG/TIFF. 

Try converting the image again with a different tool, or if it is in the desired format, open it in an image editing tool and try exporting a new copy from there.