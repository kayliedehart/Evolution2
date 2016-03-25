import unittest
from dealer import *
from species import Species
from playerState import PlayerState
from traitCard import TraitCard
from jsonParsing import *

class TestDealer(unittest.TestCase):

	def setUp(self):
		self.vegHorns = Species(1, 2, 3, ["horns"], 0)
		self.vegCoop = Species(1, 2, 3, ["cooperation"], 0)
		self.fat = Species(4, 3, 4, ["fat-tissue"], 3)
		self.fatScav = Species(2, 3, 4, ["fat-tissue", "scavenger"], 1)
		self.fatFor = Species(4, 3, 4, ["fat-tissue", "foraging"], 1)
		self.carnCoop = Species(3, 4, 5, ["carnivore", "cooperation"], 0)
		self.carnForage = Species(3, 4, 5, ["carnivore", "foraging"], 0)
		self.carnForage1 = Species(3, 4, 5, ["carnivore", "foraging"], 0)
		self.p1 = PlayerState(1, 0, [self.vegCoop, self.fat, self.carnForage], [])
		self.p2 = PlayerState(2, 0, [self.vegHorns, self.fatScav, self.carnCoop], [])
		self.p3 = PlayerState(3, 0, [self.vegCoop, self.carnCoop, self.carnForage1], [])
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

		self.x41 = Species(0, 5, 2, ["carnivore", "cooperation"], 0)
		self.x42 = Species(0, 5, 2, ["carnivore"], 0)
		self.x4p1 = PlayerState(1, 0, [self.x41, self.x42], [])

		self.x43 = Species(0, 2, 2, ["scavenger", "foraging", "cooperation"], 0)
		self.x44 = Species(0, 5, 1, ["carnivore", "cooperation"], 0)
		self.x4p2 = PlayerState(2, 0, [self.x43, self.x44], [])

		self.x45 = Species(0, 4, 1, [], 0)
		self.x4p3 = PlayerState(3, 0, [self.x45], [])

		self.x4d = Dealer([self.x4p1, self.x4p2, self.x4p3], 10, [])

		self.x61 = Species(0, 5, 3, ["carnivore", "cooperation", "foraging"], 0)
		self.x62 = Species(0, 5, 2, ["foraging", "carnivore"], 0)
		self.x6p1 = PlayerState(1, 0, [self.x61, self.x62], [])

		self.x63 = Species(0, 2, 1, ["scavenger", "foraging", "cooperation"], 0)
		self.x64 = Species(0, 5, 2, ["carnivore", "cooperation"], 0)
		self.x6p2 = PlayerState(2, 0, [self.x63, self.x64], [])

		self.x65 = Species(0, 4, 2, ["scavenger"], 0)
		self.x6p3 = PlayerState(3, 0, [self.x65], [])

		self.x6deal = Dealer([self.x6p1, self.x6p2, self.x6p3], 8, [])


	def tearDown(self):
		del self.vegHorns 
		del self.vegCoop
		del self.fat
		del self.fatScav 
		del self.carnCoop
		del self.carnForage
		del self.carnForage1
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
		self.xstep3deal.feed1()
		self.assertEqual(self.xstep3spec.food, 2)
		self.assertEqual(self.xstep3deal.wateringHole, 3)

		self.x4d.feed1()
		self.assertEqual(self.x41.food, 1)
		self.assertEqual(self.x42.food, 1)
		self.assertEqual(self.x43.food, 2)
		self.assertEqual(self.x44.food, 2)
		self.assertEqual(self.x4d.wateringHole, 4)

		self.x6deal.feed1()
		self.assertEqual(self.x61.food, 2)
		self.assertEqual(self.x62.food, 2)
		self.assertEqual(self.x63.food, 2)
		self.assertEqual(self.x64.food, 1)
		self.assertEqual(self.x65.food, 1)
		self.assertEqual(self.x6deal.wateringHole, 0)


	def testFeedFromWateringHole(self):
		self.assertEqual(self.dealer.wateringHole, 3)
		self.dealer.feedFromWateringHole(self.p1, 2)
		self.assertEqual(self.dealer.wateringHole, 1)
		self.assertEqual(self.carnForage.food, 5)

		self.assertEqual(self.dealer.wateringHole, 1)
		self.assertEqual(self.vegCoop.food, 1)
		self.assertEqual(self.carnCoop.food, 3)
		self.dealer.feedFromWateringHole(self.p3, 0)
		self.assertEqual(self.dealer.wateringHole, 0)
		self.assertEqual(self.vegCoop.food, 2)
		self.assertEqual(self.carnCoop.food, 3)

		self.dealer.wateringHole = 3
		self.assertEqual(self.carnForage1.food, 3)
		self.dealer.feedFromWateringHole(self.p3, 0)
		self.assertEqual(self.vegCoop.food, 3)
		self.assertEqual(self.carnCoop.food, 4)
		self.assertEqual(self.carnForage1.food, 4)
		self.assertEqual(self.dealer.wateringHole, 0)

	def testExecuteAttack(self):
		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.vegCoop.population, 3)
		self.assertEqual(self.carnCoop.food, 3)

		self.dealer.executeAttack(self.p3, self.p1, 1, 0)
		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.vegCoop.population, 2)
		self.assertEqual(self.carnCoop.food, 4)
		self.assertEqual(self.dealer.wateringHole, 0)

		self.dealer.executeAttack(self.p3, self.p2, 1, 0)
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

		self.carnCoop.traits.append("scavenger")
		self.vegCoop.traits.append("scavenger")
		self.assertEqual(self.vegCoop.food, 1)
		self.assertEqual(self.carnCoop.food, 3)
		self.dealer.scavengeFeed(self.p1)
		self.assertEqual(self.vegCoop.food, 2)
		self.assertEqual(self.carnCoop.food, 3)
		self.assertEqual(self.dealer.wateringHole, 0)


	def testFeed1(self):
		self.assertEqual(self.vegCoop.food, 1)
		self.dealer.feed1()
		self.assertEqual(self.vegCoop.food, 2)
		self.assertEqual(self.dealer.wateringHole, 2)

		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.carnCoop.food, 3)
		self.assertEqual(self.vegHorns.population, 3)
		self.p2dealer.feed1()
		self.assertEqual(self.carnCoop.population, 4)
		self.assertEqual(self.carnCoop.food, 4)
		self.assertEqual(self.vegHorns.population, 2)

		self.assertEqual(self.fatFor.fatFood, 1)
		self.assertEqual(self.fatFor.food, 4)
		self.p3dealer.feed1()
		self.assertEqual(self.fatFor.fatFood, 3)
		self.assertEqual(self.fatFor.food, 4)
		self.assertEqual(self.p3dealer.wateringHole, 1)

		# a user without any species should not be deleted from players
		# but should be deleted from currentlyFeeding 
		# 0067-2657-1
		pNoSpecies1 = PlayerState(1, 0, [], [])
		pNoSpecies2 = PlayerState(2, 0, [], [])
		pNoSpecies3 = PlayerState(3, 0, [], [])
		dNoSpecies = Dealer([pNoSpecies1, pNoSpecies2, pNoSpecies3], 5, [])
		self.assertEqual(len(dNoSpecies.players), 3)
		self.assertEqual(len(dNoSpecies.currentlyFeeding), 3)
		dNoSpecies.feed1()
		self.assertEqual(len(dNoSpecies.players), 3)
		self.assertEqual(len(dNoSpecies.currentlyFeeding), 2)
		self.assertFalse(pNoSpecies1 in dNoSpecies.currentlyFeeding)

		# a user who can no longer attack/feed should not be deleted from players
		# but should be deleted from currentlyFeeding 
		# 0067-2657-7
		pNoAtkSpecies1 = PlayerState(1, 0, [Species(0, 1, 1, ["carnivore"], 0), 
					Species(1, 1, 1, ["horns", "cooperation"], 0), 
					Species(1, 1, 1, [], 0)], [])
		pNoAtkSpecies2 = PlayerState(2, 0, [Species(0, 1, 1, ["hard-shell"], 0)], [])
		pNoAtkSpecies3 = PlayerState(3, 0, [Species(0, 1, 1, ["cooperation", "scavenger", "climbing"], 0), 
					Species(0, 1, 2, ["cooperation", "scavenger", "climbing"], 0), 
					Species(0, 1, 4, ["foraging", "hard-shell"], 0)], [])
		dNoAtkSpecies = Dealer([pNoAtkSpecies1, pNoAtkSpecies2, pNoAtkSpecies3], 5, [])
		self.assertEqual(len(dNoAtkSpecies.players), 3)
		self.assertEqual(len(dNoAtkSpecies.currentlyFeeding), 3)
		dNoAtkSpecies.feed1()
		self.assertEqual(len(dNoAtkSpecies.players), 3)
		self.assertEqual(len(dNoAtkSpecies.currentlyFeeding), 2)
		self.assertFalse(pNoAtkSpecies1 in dNoAtkSpecies.currentlyFeeding)

		# successfully extincting someone else's species should give two cards to loser
		# 2598-3830-8
		pExtinction1 = PlayerState(3, 2, [Species(3, 4, 4, ["carnivore"], 0)], [TraitCard("burrowing", -3)])
		pExtinction2 = PlayerState(2, 42, [Species(0, 3, 4, ["climbing"], 0),
					Species(4, 2, 4, ["climbing"], 0),
					Species(4, 1, 4, ["climbing"], 0)], [TraitCard("climbing", 3)])
		pExtinction3 = PlayerState(4, 100, [Species(0, 7, 1, [], 0)], [])
		dExtinction = Dealer([pExtinction1, pExtinction2, pExtinction3], 9, [TraitCard("burrowing", 3), TraitCard("horns", 3), TraitCard("climbing", 1)])

		self.assertEqual(len(dExtinction.deck), 3)
		dExtinction.feed1()
		self.assertEqual(len(dExtinction.deck), 1)
		self.assertEqual(pExtinction3.hand, [TraitCard("burrowing", 3), TraitCard("horns", 3)])
		self.assertEqual(len(pExtinction3.species), 0)
		self.assertEqual(pExtinction1.species[0].food, 4)
		self.assertEqual(dExtinction.wateringHole, 8)

		# cooperation + foraging + scavenging
		# 8949-0357-4
		pCFS1 = PlayerState(1, 3, [Species(4, 2, 5, ["carnivore", "cooperation"], 0), 
			Species(1, 3, 4, ["foraging", "carnivore", "scavenger"], 0)], [])
		pCFS2 = PlayerState(2, 4, [Species(2, 3, 3, ["burrowing"], 0)], [])
		pCFS3 = PlayerState(3, 5, [], [])
		dCFS = Dealer([pCFS1, pCFS2, pCFS3], 10, [])

		dCFS.feed1()
		self.assertEqual(pCFS1.species[0].food, 5)
		self.assertEqual(pCFS1.species[1].food, 4)
		self.assertEqual(pCFS2.species[0].population, 2)
		self.assertEqual(dCFS.wateringHole, 6)


	def testMatthias(self):
		pass

if __name__ == "__main__":
	unittest.main()
