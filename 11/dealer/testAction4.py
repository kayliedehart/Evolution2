# Unit tests for the Attack4 request types
import unittest
from action4 import Action4
from gainPopulation import GainPopulation
from gainBodySize import GainBodySize
from buySpeciesBoard import BuySpeciesBoard
from replaceTrait import ReplaceTrait
from playerState import PlayerState
from species import Species
from traitCard import TraitCard

class TestAction4(unittest.TestCase):
	def setUp(self):
		self.t1 = TraitCard("horns", 3)
		self.t2 = TraitCard("ambush", 1)
		self.t3 = TraitCard("carnivore", 2)
		self.t4 = TraitCard("fat-tissue", 0)
		self.t5 = TraitCard("foraging", 3)
		self.t6 = TraitCard("herding", 0)
		self.defSpec = Species(0, 0, 1, [], 0)
		self.specWGrownBody = Species(0, 1, 1, [], 0)
		self.specW3t = Species(0, 0, 1, [self.t3, self.t4, self.t5], 0)
		self.specWAll = Species(0, 1, 2, [self.t4], 0)
		self.playerWithManyCards = PlayerState(1, 0, [], [self.t1, self.t2, self.t3, self.t4, self.t5, self.t6])
		self.playerForAll = PlayerState(1, 0, [self.specWAll], [])
		self.playerFor3t = PlayerState(1, 0, [self.specW3t], [self.t6])
		self.playerForDefSpec = PlayerState(1, 0, [self.defSpec], [self.t5, self.t6])
		self.playerForBodyNewspec = PlayerState(1, 0, [self.specWGrownBody], [self.t3, self.t4, self.t5, self.t6])
		self.noAct = Action4(0, [], [], [], [])
		self.actGP = Action4(0, [GainPopulation(0, 1)], [], [], [])
		self.actGB = Action4(0, [], [GainBodySize(0, 1)], [], [])
		self.actRT = Action4(0, [], [], [ReplaceTrait(0, 1, 1)], [])
		self.actBT0t = Action4(0, [], [], [], [BuySpeciesBoard(1, [])])
		self.actBT1t = Action4(0, [], [], [], [BuySpeciesBoard(1, [2])])
		self.actBT2t = Action4(0, [], [], [], [BuySpeciesBoard(1, [2, 3])])
		self.actBT3t = Action4(0, [], [], [], [BuySpeciesBoard(1, [2, 3, 4])])
		self.actBT4t = Action4(0, [], [], [], [BuySpeciesBoard(1, [2, 3, 4, 5])])
		self.addBodyToNewSpec = Action4(0, [GainPopulation(1, 1)], [], [], [BuySpeciesBoard(2, [3])])
		self.actAll = Action4(0, [GainPopulation(0, 1)], [GainBodySize(0, 2)], [ReplaceTrait(0, 0, 3)], [BuySpeciesBoard(4, [5])])
		

	def tearDown(self):
		del self.t1
		del self.t2
		del self.t3
		del self.t4
		del self.t5
		del self.t6
		del self.defSpec
		del self.specWGrownBody
		del self.specW3t
		del self.specWAll
		del self.playerWithManyCards
		del self.playerFor3t
		del self.playerForAll
		del self.playerForDefSpec
		del self.playerForBodyNewspec
		del self.noAct
		del self.actGP
		del self.actGB
		del self.actRT
		del self.actBT0t
		del self.actBT1t
		del self.actBT2t
		del self.actBT3t
		del self.actBT4t
		del self.addBodyToNewSpec
		del self.actAll		


	def testActionFromJson(self):

	def testValidate(self):
		pass


class TestGainPopulation(unittest.TestCase):
	def setUp(self):
		self.GP1 = 
		self.GP2 = 
		self.GP3 = 
		self.GP4 = 
		self.GP5 = 
		

	def tearDown(self):
		del self.GP1 
		del self.GP2
		del self.GP3
		del self.GP4
		del self.GP5


	def testFromJson(self):

	def testValidate(self):
		pass
	


class TestGainBodySize(unittest.TestCase):
	def setUp(self):
		self.GB1 = 
		self.GB2 = 
		self.GB3 = 
		self.GB4 = 
		self.GB5 = 
		

	def tearDown(self):
		del self.GB1 
		del self.GB2
		del self.GB3
		del self.GB4
		del self.GB5


	def testFromJson(self):

	def testValidate(self):
		pass
		

class TestBuySpeciesBoard(unittest.TestCase):
	def setUp(self):
		self.BT1 = 
		self.BT2 = 
		self.BT3 = 
		self.BT4 = 
		self.BT5 = 
		

	def tearDown(self):
		del self.BT1 
		del self.BT2
		del self.BT3
		del self.BT4
		del self.BT5


	def testFromJson(self):

	def testValidate(self):
		pass


class TestReplaceTrait(unittest.TestCase):
	def setUp(self):
		self.RT1 = 
		self.RT2 = 
		self.RT3 = 
		self.RT4 = 
		self.RT5 = 
		

	def tearDown(self):
		del self.RT1 
		del self.RT2
		del self.RT3
		del self.RT4
		del self.RT5


	def testFromJson(self):

	def testValidate(self):
		pass
		
		

if __name__ == "__main__":
	unittest.main()
