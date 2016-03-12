import os
import glob
import json
import unittest
from jsonParsing import *

HW_5_TEST_PATH = "homework_5_tests/"

class testFest(unittest.TestCase):

    def testHw5(self):
        os.chdir("../..")
        os.chdir(HW_5_TEST_PATH)
        inFiles = glob.glob("*-in.json")
        outFiles = glob.glob("*-out.json")
        os.chdir("..")
        # Loop through the files in homework_5_tests directory and make sure inputs match expected outputs
        for i in range(len(inFiles)):
            inFileName = inFiles[i].replace("-in.json", "")
            outFileName = outFiles[i].replace("-out.json", "")
            # Make sure that these are the same corresponding test files
            self.assertEquals(inFileName, outFileName)
            if inFileName == outFileName:
                with open(HW_5_TEST_PATH + inFiles[i], 'r') as input:
                    with open(HW_5_TEST_PATH + outFiles[i], 'r') as output:
                        input = json.load(input)
                        output = json.load(output)
                        defend, attack, lNeighbor, rNeighbor = JsonParsing.situationFromJson(input)
                        self.assertEqual(Species.isAttackable(defend, attack, lNeighbor, rNeighbor), output)



if __name__ == "__main__":
    unittest.main()
