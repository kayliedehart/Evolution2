#!/usr/bin/env python2.7

import sys
import subprocess

TEST_PATH = "feeding/feed_tests/"
PYTHON2_PATH = "python2.7"


def xfeed(testName, fileName):
    printing = testName + "\n\tresult: "
    try:
        result = subprocess.check_output([PYTHON2_PATH, sys.path[0] + "/xfeed"], stdin=fileName)
        if not result:
            printing += "program quit\n"
        else:
            printing += result
    except Exception as e:
        printing += str(e)

    print printing


with open(TEST_PATH + "/bad-io-in.json", "r") as badIO:
    xfeed("gibberish input (xfeed should quit)", badIO)

with open(TEST_PATH + "/bad-input-in.json", "r") as badJson:
    xfeed("bad json input (xfeed should quit)", badJson)

with open(TEST_PATH + "attackTest1-in.json", "r") as att1:
    xfeed("test a carnivore attack (should be some json)", att1)

with open(TEST_PATH + "fatTissueTest1-in.json", "r") as fat1:
    xfeed("test a fat tissue feeding (should be some json)", fat1)

with open(TEST_PATH + "testVeg1-in.json", "r") as veg1:
    xfeed("test a vegetarian feeding (should be some json)", veg1)
