# KAD

- [Requirements](#requirements)
    - [Installation](#installation)
    - [Overview](#overview)
- [Usage](#usage)
    - [Image Quality Evaluation (IQE) Software](#image-quality-evaluation-iqe-software)
    - [Config](#config)
    - [Running](#running)
    - [Connect](#connect)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

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

## API Documentation

The API documentation is made to be displayed with Mkdocs. All pages are contained within [`docs/`](docs/), and the configuration is found in [`mkdocs.yml`](mkdocs.yml)

It can be dynamically served with:
```
mkdocs serve
```

Or statically built with:
```
mkdocs build
```

## Troubleshooting

TBD