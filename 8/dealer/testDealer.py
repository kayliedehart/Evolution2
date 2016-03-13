import unittest
from dealer import *
from species import Species
from playerState import PlayerState

class TestDealer(unittest.TestCase):

	def setUp(self):
		self.vegHorns = Species(1, 2, 3, ["horns"], 0)
		self.vegCoop = Species(1, 2, 3, ["cooperation"], 0)
		self.fat = Species(4, 3, 4, ["fat-tissue"], 3)
		self.fatScav = Species(2, 3, 4, ["fat-tissue", "scavenging"], 1)
		self.fatFor = Species(2, 3, 4, ["fat-tissue", "foraging"], 1)
		self.carnCoop = Species(3, 4, 5, ["carnivore", "cooperation"], 0)
		self.carnForage = Species(3, 4, 5, ["carnivore", "foraging"], 0)
		self.p1 = PlayerState(1, 0, [self.vegCoop, self.fat, self.carnForage], [])
		self.p2 = PlayerState(2, 0, [self.vegHorns, self.fatScav, self.carnCoop], [])
		self.p3 = PlayerState(3, 0, [self.vegCoop, self.carnCoop, self.carnForage], [])
		self.p4 = PlayerState(4, 0, [self.vegCoop], [])
		self.p5 = PlayerState(5, 0, [self.vegHorns], [])
		self.p6 = PlayerState(6, 0, [self.carnCoop], [])
		self.p7 = PlayerState(7, 0, [self.fatScav], [])
		self.p8 = PlayerState(8, 0, [self.fatFor], [])
		self.dealer = Dealer([self.p1, self.p2, self.p3], 3, [])
		self.p2dealer = Dealer([self.p6, self.p5], 3, [])
		self.p3dealer = Dealer([self.p8], 3, [])


		self.xstep3spec = Species(0, 5, 2, ["foraging"], 0)
		self.xstep3p = PlayerState(1, 0, [self.xstep3spec], [])
		self.xstep3deal = Dealer([self.xstep3p], 5, [])

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
		del self.p4
		del self.p5
		del self.p6
		del self.p7
		del self.p8
		del self.dealer
		del self.p2dealer
		del self.p3dealer

		del self.xstep3spec
		del self.xstep3p
		del self.xstep3deal

	def testXstep(self):
		self.assertEqual(self.xstep3spec.food, 0)
		self.xstep3deal.feed1(self.xstep3deal.players)
		self.assertEqual(self.xstep3spec.food, 2)
		self.assertEqual(self.xstep3deal.wateringHole, 3)

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
		self.assertEqual(self.dealer.wateringHole, 0)
		self.assertEqual(self.vegCoop.food, 3)
		self.assertEqual(self.carnCoop.food, 4)

	def testExecuteAttack(self):
		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.vegCoop.population, 3)
		self.assertEqual(self.carnCoop.food, 3)

		self.dealer.executeAttack(self.p3, self.p1, self.carnCoop, self.vegCoop)
		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.vegCoop.population, 2)
		self.assertEqual(self.carnCoop.food, 4)
		self.assertEqual(self.dealer.wateringHole, 0)

		self.dealer.executeAttack(self.p3, self.p2, self.carnCoop, self.vegHorns)
		self.assertEqual(self.carnCoop.population, 4)
		self.assertEqual(self.vegHorns.population, 2)

	def testAutoFeed(self):
		self.assertFalse(self.dealer.autoFeed(self.p1))

		self.assertFalse(self.dealer.autoFeed(self.p2))
		
		self.assertEqual(self.vegCoop.food, 1)
		self.assertTrue(self.dealer.autoFeed(self.p4))
		self.assertEqual(self.vegCoop.food, 2)
		
	def testQueryFeed(self):
		self.assertEqual(self.vegCoop.food, 1)
		self.assertFalse(self.dealer.queryFeed(self.p4))
		self.assertEqual(self.vegCoop.food, 2)

		self.assertEqual(self.fatScav.fatFood, 1)
		self.assertFalse(self.dealer.queryFeed(self.p7))
		self.assertEqual(self.fatScav.fatFood, 3)
		self.assertEqual(self.dealer.wateringHole, 0)

		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.carnCoop.food, 3)
		self.assertEqual(self.vegHorns.population, 3)
		self.assertTrue(self.p2dealer.queryFeed(self.p6))
		self.assertEqual(self.carnCoop.population, 4)
		self.assertEqual(self.carnCoop.food, 4)
		self.assertEqual(self.vegHorns.population, 2)

	def testScavengeFeed(self):
		self.assertEqual(self.fatScav.food, 2)
		self.assertEqual(self.dealer.wateringHole, 3)
		self.dealer.scavengeFeed(self.p1)
		self.assertEqual(self.fatScav.food, 3)
		self.assertEqual(self.dealer.wateringHole, 2)

		self.dealer.scavengeFeed(self.p1)
		self.dealer.scavengeFeed(self.p1)
		self.dealer.scavengeFeed(self.p1)
		self.assertEqual(self.fatScav.food, 4)
		self.assertEqual(self.dealer.wateringHole, 1)

		self.carnCoop.traits.append("scavenging")
		self.vegCoop.traits.append("scavenging")
		self.assertEqual(self.vegCoop.food, 1)
		self.assertEqual(self.carnCoop.food, 3)
		self.dealer.scavengeFeed(self.p1)
		self.assertEqual(self.vegCoop.food, 2)
		self.assertEqual(self.carnCoop.food, 3)
		self.assertEqual(self.dealer.wateringHole, 0)


	def testFeed1(self):
		self.assertEqual(self.vegCoop.food, 1)
		self.dealer.feed1(self.dealer.players)
		self.assertEqual(self.vegCoop.food, 2)
		self.assertEqual(self.dealer.wateringHole, 2)

		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.carnCoop.food, 3)
		self.assertEqual(self.vegHorns.population, 3)
		self.p2dealer.feed1(self.p2dealer.players)
		self.assertEqual(self.carnCoop.population, 4)
		self.assertEqual(self.carnCoop.food, 4)
		self.assertEqual(self.vegHorns.population, 2)

		self.assertEqual(self.fatFor.fatFood, 1)
		self.assertEqual(self.fatFor.food, 2)
		self.p3dealer.feed1(self.p3dealer.players)
		self.assertEqual(self.fatFor.fatFood, 3)
		self.assertEqual(self.fatFor.food, 3)
		self.assertEqual(self.p3dealer.wateringHole, 0)

if __name__ == "__main__":
	unittest.main()
