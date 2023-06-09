#!/usr/bin/env python
#
# dpt.py - Data Processing Tool
# Joseph P Day
# Created 17 MAY 2023
# v0.1.6   5 JUN 2023    Reconfigure functions for pytest
#

"""Data Processing Tool."""

import json
import os
import sys


# import typing
# import re
# import pandas as pd


class Dpt:
    """Data processing tool migration from SAS."""

    current_state_num = 0
    json_data = ""
    json_file = ""

    machine_states = (
        "init",
        "create_project_subfolders",
        "new_program_calls",
        "read_lab_pro_qc",
        "process_data_inputs",
    )

    tlog: list[str] = []

    def __init__(self, json_file: str) -> None:
        """Initialize the class.

        Create class vars using JSON from file location provided.

        Parameters
        ----------
        json_file : str
            The path where the process was started.

        Raises
        ------
        FileNotFoundError
            Error: [err]

        Returns
        -------
        None

        """
        # print("initializing....")
        self.home_dir = os.getcwd()
        self.json_file = json_file

        jfile = self.check_json(json_file)

        if jfile == "":
            print(f"Error: JSON file {self.json_file} not found")
            return None

        self.input_json = jfile
        self.json_data = self.read_json(self.input_json)
        print(f"got json_data: \n{self.json_data}")
        if self.json_data == "":
            return None

        self.load_json(self.json_data)

    def read_json(self, json_file: str) -> str:
        """Read the __init__ JSON file.

        Extract the contents of the JSON file.

        Parameters
        ----------
        json_file : str
            The JSON file to be read containing class vars to be created.

        Raises
        ------
        Exception
            Error: Unexpected ([err])

        Returns
        -------
        str
            The contents of the JSON file

        """

        try:
            print(f"open {json_file}")
            with open(json_file, encoding="utf-8") as jfp:
                return jfp.read()
        except Exception as err:
            print(f"Error: Unexpected ({err})")
            return ""

    def load_json(self, jdata: str) -> None:
        """Load the data from the JSON file.

        Parse the JSON text to create class variables.

        Parameters
        ----------
        jdata: str
            The raw JSON text.

        Raises
        ------
        ValueError
            Error: Malformed JSON in {jdata} ([err])
        SyntaxError
            Error: Data type problem in {jdata} ([err])
        UnicodeDecodeError
            Error: Failed to recognize unicode in {jdata} ([err])
        NameError
            Error: Failed to assign class var [index] ([err])

        Returns
        -------
        None

        """

        try:
            dat = json.loads(jdata)
        except ValueError as err:
            print(f"Error: Malformed JSON in {jdata} ({err})")
            self.end("E2")
        except SyntaxError as err:
            print(f"Error: Data type problem in {jdata} ({err})")
            self.end("E2")
        except UnicodeDecodeError as err:
            print(f"Warning: Failed to recognize unicode in {jdata} ({err})")
            self.end("W4")
        except Exception as err:
            print(f"Error: unspecified ({err})")
            self.end("E2")

        for k in dat:
            # self.tlog.append(f"self.{k} = dat[\"{k}\"]")
            try:
                exec(f'self.{k} = dat["{k}"]')
            except NameError as err:
                print(f"Error: Failed to assign class var {k} ({err})")
                self.end("E3")

    def end(self, errcode: str = "0") -> None:
        """End the process.

        Try to end gracefully, and provide an error code.

        Parameters
        ----------
        errcode : str
            Exit and provide the error code. Default 0, no error.

        Exit
        ----
        int
            Exit passing the error code.

        Returns
        -------
        None

        """
        self.addlog(errcode)
        self.getlog()
        sys.exit(errcode)

    def check_json(self, json_file: str) -> str:
        """Find the JSON file.

        Check whether the json_file can be found. If not found, try adding
        home_dir to the front of the path and recheck.

        Parameters
        ----------
        json_file : str
            The location of the JSON file passed to the class. Format: <path>/file_name

        Raises
        ------
        FileNotFoundError
            JSON file {json_file} not found

        Returns
        -------
        str
            The full path and file name where the JSON file was found.

        """
        if os.path.exists(json_file):
            return json_file

        jfile = f"{self.home_dir}/{json_file}"
        # self.tlog.append(jfile)
        if os.path.exists(jfile):
            return jfile
        else:
            return ""

    def addlog(self, msg: str = "unk") -> None:
        """Add a message to the log.

        Capture a diagnostic message.

        Parameters
        ----------
        msg : str
            A string for the message to be appended to tlog

        Returns
        -------
        None

        """
        self.tlog.append(msg)

    def getlog(self) -> None:
        """Diagnostic log for dev.

        Development tool to display diagnostic messages.

        Returns
        -------
        None

        """
        for line in self.tlog:
            print(f"{line}")


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
# v0.1.6   5 JUN 2023    Reconfigure functions for pytest
# v0.1.5  30 MAY 2023    Function as imported module, cleaner for testing
# v0.1.4  23 MAY 2023    Adding type annotations, 4 sp/tab
# v0.1.3  22 MAY 2023    Adding Docstrings, Numpystyle
# v0.1.2  19 MAY 2023    Apply Flake8,Pylint,Isort and correct as needed.
# v0.1.1  19 MAY 2023    Specify JSON input file, check exists
# v0.1.0  17 MAY 2023    New
#
#############################
