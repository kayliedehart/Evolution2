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


with open(TEST_PATH + "/xstep_in_1.json", "r") as one:
    xstep("regular configuration; expected output: one configuration", one)

with open(TEST_PATH + "/xstep_invalid.json", "r") as invalid:
    xstep("bad json; expected output: none", invalid)	

with open(TEST_PATH + "/xstep_invalid_players.json", "r") as invalidPlayers:
    xstep("invalid json players; expected output: none", invalidPlayers)	
