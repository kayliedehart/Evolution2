import os
import glob
import json
import unittest
from jsonParsing import *
from player import *

CUR_DIR = os.getcwd()
HW_5_TEST_PATH = "homework_5_tests/"
HW_6_TEST_PATH = "homework_6_tests/"
HW_7_TEST_PATH = "homework_7_tests/"


class testFest(unittest.TestCase):

	def setUp(self):
		os.chdir("../..")

	def tearDown(self):
		os.chdir(CUR_DIR)

	def testHw5(self):
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

	def testHw6(self):
		os.chdir(HW_6_TEST_PATH)
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
				with open(HW_6_TEST_PATH + inFiles[i], 'r') as input:
					with open(HW_6_TEST_PATH + outFiles[i], 'r') as output:
						if os.stat(outFiles[i]).st_size > 0:
							output = json.load(output)
						else:
							output = False
						input = json.load(input)
						curState = JsonParsing.playerStateFromJson(input[0])
						wateringHole = input[1]
						others = []
						for player in input[2]:
							others.append(JsonParsing.playerStateFromJson(player))
						self.assertEqual(Player.feed(curState, wateringHole, others), output)

	def testHw7(self):
		os.chdir(HW_7_TEST_PATH)
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
				with open(HW_7_TEST_PATH + inFiles[i], 'r') as input:
					with open(HW_7_TEST_PATH + outFiles[i], 'r') as output:
						if os.stat(outFiles[i]).st_size > 0:
							output = json.load(output)
						else:
							output = False
						input = json.load(input)
						curState = JsonParsing.playerStateFromJson(input[0])
						wateringHole = input[1]
						others = []
						for player in input[2]:
							others.append(JsonParsing.playerStateFromJson(player))
						self.assertEqual(Player.feed(curState, wateringHole, others), output)




if __name__ == "__main__":
	unittest.main()
