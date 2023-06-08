#!/usr/bin/env python
#
# adreg.py - run AD jobs
# Joseph P Day
# Created 30 MAY 2023
# v0.1.0  30 MAY 2023    more....
#

"""Data Processing Tool."""

from adpt import dpt


JSON_INPUT_FILE = "test_input_v1.json"

dd = dpt.Dpt(JSON_INPUT_FILE)

# dd.getlog()

# Error codes
#############################
#
# 1   File not found
# 2   File JSON has incorrect format
# 3   Cannot assign class var from JSON data
# 4   JSON data contains invalid unicode
#
#############################

# Version History
#############################
#
# v0.1.4  23 MAY 2023    Adding type annotations, 4 sp/tab
# v0.1.3  22 MAY 2023    Adding Docstrings, Numpystyle
# v0.1.2  19 MAY 2023    Apply Flake8,Pylint,Isort and correct as needed.
# v0.1.1  19 MAY 2023    Specify JSON input file, check exists
# v0.1.0  17 MAY 2023    New
#
#############################
