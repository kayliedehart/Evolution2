#!/usr/bin/env python2.7

import sys
import subprocess

TEST_PATH = "json-tests"
PYTHON2_PATH = "python2.7"


def xstep(testName, fileName):
    printing = testName + "\n\tresult: "
    try:
        result = subprocess.check_output([PYTHON2_PATH, sys.path[0] + "/xstep"], stdin=fileName)
        if not result:
            printing += "program quit\n"
        else:
            printing += result
    except Exception as e:
        printing += str(e)

    print printing


with open(TEST_PATH + "/xstep-1-in.json", "r") as one:
    xstep("regular configuration; expected output: one configuration", one)

with open(TEST_PATH + "/xstep-2-in.json", "r") as two:
    xstep("regular configuration; expected output: two configuration", two)

with open(TEST_PATH + "/xstep-3-in.json", "r") as three:
    xstep("regular configuration; expected output: three configuration", three)

with open(TEST_PATH + "/xstep-4-in.json", "r") as four:
    xstep("regular configuration; expected output: four configuration", four)

with open(TEST_PATH + "/xstep-5-in.json", "r") as five:
    xstep("regular configuration; expected output: five configuration", five)

with open(TEST_PATH + "/xstep-6-in.json", "r") as six:
    xstep("regular configuration; expected output: six configuration", six)

with open(TEST_PATH + "/xstep-invalid.json", "r") as invalid:
    xstep("bad json; expected output: none", invalid)	

with open(TEST_PATH + "/xstep-invalid-players.json", "r") as invalidPlayers:
    xstep("invalid json players; expected output: none", invalidPlayers)	
