import unittest
from dealer import *
import sys
sys.path.append("../feeding")
from species import Species
from playerState import PlayerState

class TestDealer(unittest.TestCase):

	def setUp(self):
		self.vegHorns = Species(1, 2, 3, ["horns"], 0)
		self.vegCoop = Species(1, 2, 3, ["cooperation"], 0)
		self.fat = Species(4, 3, 4, ["fat-tissue"], 3)
		self.fatScav = Species(2, 3, 4, ["fat-tissue", "scavenging"], 1)
		self.carnCoop = Species(3, 4, 5, ["carnivore", "cooperation"], 0)
		self.carnForage = Species(3, 4, 5, ["carnivore", "foraging"], 0)
		self.p1 = PlayerState(1, 0, [self.vegCoop, self.fat, self.carnForage], [])
		self.p2 = PlayerState(2, 0, [self.vegHorns, self.fatScav, self.carn], [])
		self.p3 = PlayerState(3, 0, [self.vegCoop, self.carnCoop, self.carnForage], [])
		self.p4 = PlayerState(4, 0, [self.vegCoop], [])
		self.dealer = Dealer([self.p1, self.p2, self.p3], 3, [])

	def tearDown(self):
		del self.vegHorns 
		del self.vegCoop
		del self.fat
		del self.fatScav 
		del self.carnCoop
		del self.carnForage
		del self.p1 
		del self.p2
		del self.p3
		del self.dealer

	def testFeedFromWateringHole(self):
		self.assertEqual(self.dealer.wateringHole, 3)
		self.dealer.feedFromWateringHole(self.p1, self.carnForage)
		self.assertEqual(self.dealer.wateringHole, 1)
		self.assertEqual(self.carnForage.food, 5)

		self.dealer.feedFromWateringHole(self.p3, self.vegCoop)
		self.assertEqual(self.dealer.wateringHole, 0)
		self.assertEqual(self.vegCoop.food, 2)
		self.assertEqual(self.carnCoop.food, 3)

		self.dealer.wateringHole = 3
		self.dealer.feedFromWateringHole(self.p3, self.vegCoop)
		self.assertEqual(self.dealer.wateringHole, 1)
		self.assertEqual(self.vegCoop.food, 3)
		self.assertEqual(self.carnCoop.food, 4)

	def testExecuteAttack(self):
		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.vegCoop.population, 3)
		self.assertEqual(self.carnCoop.food, 3)

		self.dealer.executeAttack(self.p3, self.vegCoop, self.carnCoop)
		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.vegCoop.population, 2)
		self.assertEqual(self.carCoop.food, 4)
		self.assertEqual(self.dealer.wateringHole, 2)

		self.dealer.executeAttack(self.p3, self.vegHorns, self.carnCoop)
		self.assertEqual(self.carnCoop.population, 4)
		self.assertEqual(self.vegHorns.population, 2)

	def testAutoFeed(self):
		self.assertFalse(self.dealer.autoFeed(self.p1))
		self.assertTrue(self.dealer.autoFeed(self.p4))
		# TODO

	def testQueryFeed(self):
		pass

	def testScavengeFeed(self):
		pass

	def testFeed1(self):
		pass

if __name__ == "__main__":
	unittest.main()
