import json
import os

import pytest

from adpt import dpt

JSON_INPUT_FILE = "test_input_v1.json"
dd = dpt.Dpt(JSON_INPUT_FILE)

inputj = {
  "reportset":"Orig",
  "wavelength":"590a",
  "Alist":["H","He","Li","Be","B","C","N","O","F","Ne"],
  "prodfam":"Neg",
  "design":"B",
  "doggenus":"Canus",
  "dogtype":"hound",
  "foodog":"Ruffles",
  "dogname":"Astro",
  "wacut":900,
  "wucut":200,
  "inputspecver":7,
  "study":"staying",
  "studytype":"obedience",
  "studyabbr":"Obed",
  "breakpnt":"barking",
  "phase":"bone",
  "map_phase":"bury_bone",
  "heeltest":"0.50 miles",
  "group_set":"inputs.calm_dogs",
  "test_set":"inputs.nervous_dog",
  "qcdog":"retreiver",
  "firstset":"inputs.old_dog",
  "header1":"Dog training solo and in groups",
  "dog_run_lot":"Woodland Park dog run",
  "PDdogs":"K9 units",
  "CSIver":"cadaver sniffing",
  "EUver":"doberman",
  "report_type":"Breed",

  "studypath":"C:\\Projects\\Dogs\\training",
  "DTQC":"G:\\Data\\Dogs\\training\\dataset",

  "inputloc":"C:\\Projects\\Dogs\\locations",
  "DOGfile":"C:\\Projects\\Dogs\\Input Specs\\dog_breed_behaviors.xlsx",
  "dogdataloc":"C:\\Projects\\Dogs\\sasdata",
  "libname_in":"&dogdataloc",
  "data_path":"G:\\Data\\Dogs\\training\\obedience\\dataset",
  "feasmode":"C:\\Projects\\Dogs\\_Variability\\Input Specs\\training_results.xlsx",

  "outputloc":"C:\\Projects\\Dogs\\Characterization\\training\\Reports",
  "output_filename":"&dogname._D_&dogtype._F_&study._&breakpnt._&report_type._&sysdate..xml",
  "outfile":"&outputloc.&output_filename.",
  "QCDloc1":"G:\\Data\\Dogs\\dog_to_dog_variability\\sasdata",
  "QCDloc3":"G:\\Data\\Dogs\\Data Processing\\training\\sasdata",
  "libname_RT":"&DTQC",
  "sit_seq":["2","4","8","16"],
  "heel_seq":["8","16","32"],
    "pack_size":["2","3","5","8"], 
  "stay_seq":["2","4","8","15","30","60"],
    
  "cor":{
    "dog_nums":"<compliance(dog_num,'')>",
        "species_nums":"<compliance(dog_spec,'')>"
    },
  "qccompliance":""
}


@pytest.mark.parametrize(
    "json_file",
    [
        "test_Input_v1.json",
    ],
)
def test_exists_json(json_file):
    jfile = dd.check_json(json_file)
    assert os.path.exists(jfile)


@pytest.mark.parametrize(
    "json_file",
    [
        "test_output_v1.json",
    ],
)
def test_not_found_json(json_file):
    jfile = dd.check_json(json_file)
    assert jfile == ""


"""
@pytest.mark.parametrize(

)
def test_load_json(jfile):
    json_data = load_json(jfile)
    assert json_data == 
"""


def load_tc_from_file(tc_params, tc_checks, tc_json):
    [str(x).strip() for x in tc_params.split(",")]

    def wrapper(function):
        with open(tc_json) as f:
            tc_data = json.loads(f.read())
        tc_cases = []
        function.tc_params = tc_params
        for x in tc_checks:
            if x in tc_data:
                expct = tc_data[x]
            else:
                expct = "__error__"
            tc_cases.append((tc_checks[x], expct))
        function.tc_cases = tc_cases

        return function

    return wrapper


def pytest_generate_tests(metafunc):
    val = getattr(metafunc.function, "tc_cases", None)
    if val:
        # print(f"attr of function is {val}")
        metafunc.parametrize(metafunc.function.tc_params, metafunc.function.tc_cases)


@load_tc_from_file("test_input, expected", inputj, f"./{JSON_INPUT_FILE}")
def test_equal(test_input, expected):
    assert test_input == expected
