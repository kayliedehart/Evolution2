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
		pass

	def testValidate(self):
		pass

	def testGPFromJson(self):
		pass

	def testGPValidate(self):
		pass

	def testGBFromJson(self):
		pass

	def testGBValidate(self):
		pass

	def testBTFromJson(self):
		pass

	def testBTValidate(self):
		pass

	def testRTFromJson(self):
		pass

	def testRTValidate(self):
		pass






if __name__ == "__main__":
	unittest.main()
