import unittest
from playerState import *
from traitCard import TraitCard

class TestPlayerState(unittest.TestCase):

	def setUp(self):
		self.noTraits = Species(0, 1, 3, [], 0)
		self.vegHorns = Species(1, 2, 3, ["horns"], 0)
		self.vegCoop = Species(1, 2, 3, ["cooperation"], 0)
		self.fat = Species(4, 3, 4, ["fat-tissue"], 3)
		self.full = Species(2, 2, 2, [], 0)
		self.fatScav = Species(2, 3, 4, ["fat-tissue", "scavenger"], 1)
		self.fatFor = Species(4, 3, 4, ["fat-tissue", "foraging"], 1)
		self.carnCoop = Species(3, 4, 5, ["carnivore", "cooperation"], 0)
		self.carnForage = Species(3, 4, 5, ["carnivore", "foraging"], 0)
		self.carnForage1 = Species(3, 4, 5, ["carnivore", "foraging"], 0)
		self.forCoop = Species(1, 3, 5, ["foraging", "cooperation"], 0)
		self.extinct = Species(0, 0, 0, [], 0)
		self.p1 = PlayerState(1, 0, [self.vegCoop, self.fat, self.carnForage], [])
		self.p2 = PlayerState(2, 0, [self.vegHorns, self.fatScav, self.carnCoop], [])
		self.p3 = PlayerState(3, 0, [self.vegCoop, self.carnCoop, self.carnForage1], [])
		self.p4 = PlayerState(4, 0, [self.forCoop, self.noTraits], [])
		self.p5 = PlayerState(5, 0, [self.full, self.fat], [])
		self.p6 = PlayerState(6, 0, [self.extinct], [])
		self.p7 = PlayerState(7, 0, [], [])
		self.p8 = PlayerState(8, 0, [self.carnCoop], [])
		self.p9 = PlayerState(9, 0, [self.vegHorns], [])

	def tearDown(self):
		del self.noTraits
		del self.vegHorns 
		del self.vegCoop
		del self.fat
		del self.full
		del self.fatScav 
		del self.carnCoop
		del self.carnForage
		del self.carnForage1
		del self.forCoop
		del self.extinct
		del self.p1 
		del self.p2
		del self.p3
		del self.p4
		del self.p5
		del self.p6
		del self.p7
		del self.p8
		del self.p9

	def testToDict(self):
		self.assertEqual(self.p8.toDict(), {"num": 8, "species": 
							[{"food": 3, "body": 4, "population": 5, "traits": ["carnivore", "cooperation"], "fatFood": 0}], 
							"hand": [], "foodbag": 0})
		self.assertEqual(self.p9.toDict(), {"num": 9, "species": 
							[{"food": 1, "body": 2, "population": 3, "traits": ["horns"], "fatFood": 0}], 
							"hand": [], "foodbag": 0})

	# THIS IS THE SILLY FEED!!! 
	def testFeed(self):
		self.assertEqual(self.p1.feed(5, [self.p1, self.p2, self.p3]), 0)
		self.assertEqual(self.p2.feed(5, [self.p1, self.p2, self.p3]), [1, 2])
		self.assertEqual(self.p3.feed(5, [self.p1, self.p2, self.p3]), 0)

	def testGetHungrySpecies(self):
		self.assertEqual(self.p1.getHungrySpecies(), [(0, self.vegCoop), (2, self.carnForage)])
		self.assertEqual(self.p2.getHungrySpecies(), [(0, self.vegHorns), (1, self.fatScav), (2, self.carnCoop)])
		self.assertEqual(self.p5.getHungrySpecies(), [])

	def testGetNeighbors(self):
		self.assertEqual(self.p1.getNeighbors(0), [False, self.fat])
		self.assertEqual(self.p1.getNeighbors(1), [self.vegCoop, self.carnForage])
		self.assertEqual(self.p1.getNeighbors(2), [self.fat, False])

	def testVerifyAttack(self):
		self.assertTrue(self.p1.verifyAttack(self.p2, 2, 0))
		self.assertFalse(self.p1.verifyAttack(self.p2, 1, 1))

	def testIsExtinct(self):
		self.assertTrue(self.p6.isExtinct(0))
		self.assertFalse(self.p1.isExtinct(0))

	def testRemoveSpecies(self):
		self.assertEqual(len(self.p6.species), 1)
		self.p6.removeSpecies(0)
		self.assertEqual(len(self.p6.species), 0)

	def testHasNoSpecies(self):
		self.assertTrue(self.p7.hasNoSpecies())

		self.assertFalse(self.p6.hasNoSpecies())
		self.p6.removeSpecies(0)
		self.assertTrue(self.p6.hasNoSpecies())

	def testSpeciesHasTrait(self):
		self.assertFalse(self.p6.speciesHasTrait(0, "scavenger"))
		self.assertTrue(self.p1.speciesHasTrait(0, "cooperation"))

	def testExecuteAttack(self):
		self.assertEqual(self.vegCoop.population, 3)
		self.assertEqual(self.vegCoop.food, 1)
		self.p1.executeAttack(0)
		self.assertEqual(self.vegCoop.population, 2)
		self.assertEqual(self.vegCoop.food, 1)
		self.p1.executeAttack(0)
		self.assertEqual(self.vegCoop.population, 1)
		self.assertEqual(self.vegCoop.food, 1)
		self.p1.executeAttack(0)
		self.assertEqual(self.vegCoop.population, 0)
		self.assertEqual(self.vegCoop.food, 0)

	def testFeedFatFood(self):
		self.assertEqual(self.fatScav.fatFood, 1)
		self.assertEqual(self.p2.feedFatFood(1, 2), 2)
		self.assertEqual(self.fatScav.fatFood, 3)

		self.fatScav.fatFood = 0
		self.assertEqual(self.p2.feedFatFood(1, 3), 3)
		self.assertEqual(self.fatScav.fatFood, 3)

		self.fatScav.fatFood = 2
		self.assertEqual(self.p2.feedFatFood(1, 3), 1)
		self.assertEqual(self.fatScav.fatFood, 3)

	def testFeedSpecies(self):
		self.assertEqual(self.noTraits.food, 0)
		self.p4.feedSpecies(specIdx=1, foodCount=1, wateringHole=3)
		self.assertEqual(self.noTraits.food, 1)

		self.assertEqual(self.carnForage.food, 3)
		self.p1.feedSpecies(specIdx=2, foodCount=1, wateringHole=5)
		self.assertEqual(self.carnForage.food, 5)

	def testForage(self):
		self.assertEqual(self.carnForage.food, 3)
		self.p1.forage(specIdx=2, wateringHole=4)
		self.assertEqual(self.carnForage.food, 4)

	def testCooperate(self):
		self.assertEqual(self.forCoop.food, 1)
		self.assertEqual(self.noTraits.food, 0)
		self.p4.cooperate(0, 2, 5)
		self.assertEqual(self.forCoop.food, 1)
		self.assertEqual(self.noTraits.food, 2)

	def testScavenge(self):
		self.assertEqual(self.vegHorns.food, 1)
		self.assertEqual(self.fatScav.food, 2)
		self.assertEqual(self.carnCoop.food, 3)
		self.assertEqual(self.p2.scavenge(5), 1)
		self.assertEqual(self.vegHorns.food, 1)
		self.assertEqual(self.fatScav.food, 3)
		self.assertEqual(self.carnCoop.food, 3)



if __name__ == "__main__":
	unittest.main()
