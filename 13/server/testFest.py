import os
import glob
import json
import unittest
from sillyPlayer import *
from dealer import *
from species import *
from action4 import *

CUR_DIR = os.getcwd()
HW_5_TEST_PATH = "homework_5_tests/"
HW_6_TEST_PATH = "homework_6_tests/"
HW_7_TEST_PATH = "homework_7_tests/"
HW_8_TEST_PATH = "homework_10_tests/"
HW_11_TEST_PATH = "homework_11_tests/"


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
						defend, attack, lNeighbor, rNeighbor = Species.situationFromJson(input)
						self.assertEqual(Species.isAttackable(defend, attack, lNeighbor, rNeighbor), output)

	# def testHw8(self):
	# 	os.chdir(HW_8_TEST_PATH)
	# 	inFiles = glob.glob("*-in.json")
	# 	outFiles = glob.glob("*-out.json")
	# 	os.chdir("..")
	# 	# Loop through the files in homework_8_tests directory and make sure inputs match expected outputs
	# 	for i in range(len(inFiles)):
	# 		inFileName = inFiles[i].replace("-in.json", "")
	# 		outFileName = outFiles[i].replace("-out.json", "")
	# 		# Make sure that these are the same corresponding test files
	# 		self.assertEquals(inFileName, outFileName)
	# 		if inFileName == outFileName:
	# 			with open(HW_8_TEST_PATH + inFiles[i], 'r') as input:
	# 				with open(HW_8_TEST_PATH + outFiles[i], 'r') as output:
	# 					input = json.load(input)
	# 					output = json.load(output)
	# 					input = Dealer.dealerFromJson(input)
	# 					output = Dealer.dealerFromJson(output)
	# 					input.feed1()
	# 					try:
	# 						self.assertEqual(input.dealerToJson(), output.dealerToJson())
	# 					except AssertionError as e:
	# 						print "assertionerror"
	# 						print inFileName
	# 						print input.dealerToJson()
	# 						raise e
							
	def testHw11(self):
		os.chdir(HW_11_TEST_PATH)
		inFiles = glob.glob("*-in.json")
		outFiles = glob.glob("*-out.json")
		os.chdir("..")
		# Loop through the files in homework_8_tests directory and make sure inputs match expected outputs
		for i in range(len(inFiles)):
			inFileName = inFiles[i].replace("-in.json", "")
			outFileName = outFiles[i].replace("-out.json", "")
			# Make sure that these are the same corresponding test files
			self.assertEquals(inFileName, outFileName)
			if inFileName == outFileName:
				with open(HW_11_TEST_PATH + inFiles[i], 'r') as input:
					with open(HW_11_TEST_PATH + outFiles[i], 'r') as output:
						input = json.load(input)
						output = json.load(output)
						deal = Dealer.dealerFromJson(input[0])
					 	actions = [Action4.actionFromJson(action) for action in input[1]]
						output = Dealer.dealerFromJson(output)
						deal.step4(actions)
						try:
							self.assertEqual(deal.dealerToJson(), output.dealerToJson())
						except AssertionError as e:
							print "assertionerror"
							print inFileName
							print deal.dealerToJson()
							raise e

	# def testHw6(self):
	# 	os.chdir(HW_6_TEST_PATH)
	# 	inFiles = glob.glob("*-in.json")
	# 	outFiles = glob.glob("*-out.json")
	# 	os.chdir("..")
	# 	# Loop through the files in homework_6_tests directory and make sure inputs match expected outputs
	# 	for i in range(len(inFiles)):
	# 		inFileName = inFiles[i].replace("-in.json", "")
	# 		outFileName = outFiles[i].replace("-out.json", "")
	# 		# Make sure that these are the same corresponding test files
	# 		self.assertEquals(inFileName, outFileName)
	# 		if inFileName == outFileName:
	# 			with open(HW_6_TEST_PATH + inFiles[i], 'r') as input:
	# 				with open(HW_6_TEST_PATH + outFiles[i], 'r') as output:
	# 					if os.stat(outFiles[i]).st_size > 0:
	# 						output = json.load(output)
	# 					else:
	# 						output = False
	# 					input = json.load(input)
	# 					curState = JsonParsing.playerStateFromJson(input[0])
	# 					wateringHole = input[1]
	# 					others = []
	# 					for player in input[2]:
	# 						others.append(JsonParsing.playerStateFromJson(player))
	# 					self.assertEqual(SillyPlayer.feed(curState, wateringHole, others), output)

	# def testHw7(self):
	# 	os.chdir(HW_7_TEST_PATH)
	# 	inFiles = glob.glob("*-in.json")
	# 	outFiles = glob.glob("*-out.json")
	# 	os.chdir("..")
	# 	# Loop through the files in homework_7_tests directory and make sure inputs match expected outputs
	# 	for i in range(len(inFiles)):
	# 		inFileName = inFiles[i].replace("-in.json", "")
	# 		outFileName = outFiles[i].replace("-out.json", "")
	# 		# Make sure that these are the same corresponding test files
	# 		self.assertEquals(inFileName, outFileName)
	# 		if inFileName == outFileName:
	# 			with open(HW_7_TEST_PATH + inFiles[i], 'r') as input:
	# 				with open(HW_7_TEST_PATH + outFiles[i], 'r') as output:
	# 					if os.stat(outFiles[i]).st_size > 0:
	# 						output = json.load(output)
	# 					else:
	# 						output = False
	# 					input = json.load(input)
	# 					curState = JsonParsing.playerStateFromJson(input[0])
	# 					wateringHole = input[1]
	# 					others = []
	# 					for player in input[2]:
	# 						others.append(JsonParsing.playerStateFromJson(player))
	# 					self.assertEqual(SillyPlayer.feed(curState, wateringHole, others), output)



if __name__ == "__main__":
	unittest.main()