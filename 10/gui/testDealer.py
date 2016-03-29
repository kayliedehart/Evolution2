import unittest
from dealer import *
from species import Species
from playerState import PlayerState
from traitCard import TraitCard

class TestDealer(unittest.TestCase):

	def setUp(self):
		self.t1 = TraitCard("horns", 3)
		self.t2 = TraitCard("ambush", 1)
		self.t3 = TraitCard("carnivore", 2)
		self.t4 = TraitCard("fat-tissue", 0)
		self.t5 = TraitCard("foraging", 3)
		self.vegHorns = Species(1, 2, 3, ["horns"], 0)
		self.vegCoop = Species(1, 2, 3, ["cooperation"], 0)
		self.fat = Species(4, 3, 4, ["fat-tissue"], 3)
		self.fatScav = Species(2, 3, 4, ["fat-tissue", "scavenger"], 1)
		self.fatFor = Species(4, 3, 4, ["fat-tissue", "foraging"], 1)
		self.carnCoop = Species(3, 4, 5, ["carnivore", "cooperation"], 0)
		self.carnForage = Species(3, 4, 5, ["carnivore", "foraging"], 0)
		self.carnForage1 = Species(3, 4, 5, ["carnivore", "foraging"], 0)
		self.extinct = Species(0, 0, 0, [], 0)
		self.p1 = PlayerState(1, 0, [self.vegCoop, self.fat, self.carnForage], [])
		self.p2 = PlayerState(2, 0, [self.vegHorns, self.fatScav, self.carnCoop], [])
		self.p3 = PlayerState(3, 0, [self.vegCoop, self.carnCoop, self.carnForage1], [])
		self.p4 = PlayerState(4, 0, [self.vegCoop], [])
		self.p5 = PlayerState(5, 0, [self.vegHorns], [])
		self.p6 = PlayerState(6, 0, [self.carnCoop], [])
		self.p7 = PlayerState(7, 0, [self.fatScav], [])
		self.p8 = PlayerState(8, 0, [self.fatFor, self.extinct], [])
		self.dealer = Dealer([self.p1, self.p2, self.p3], 3, [self.t1, self.t2, self.t3, self.t4, self.t5])
		self.p2dealer = Dealer([self.p6, self.p5], 3, [])
		self.p3dealer = Dealer([self.p8], 3, [self.t1, self.t2, self.t3, self.t4, self.t5])


		self.xstep3spec = Species(0, 5, 2, ["foraging"], 0)
		self.xstep3p = PlayerState(1, 0, [self.xstep3spec], [])
		self.xstep3deal = Dealer([self.xstep3p], 5, [])

		# 8949-0357-4
		self.pCFS1 = PlayerState(1, 3, [Species(4, 2, 5, ["carnivore", "cooperation"], 0), 
			Species(1, 3, 4, ["foraging", "carnivore", "scavenger"], 0)], [])
		self.pCFS2 = PlayerState(2, 4, [Species(2, 3, 3, ["burrowing"], 0)], [])
		self.pCFS3 = PlayerState(3, 5, [], [])
		self.dCFS = Dealer([self.pCFS1, self.pCFS2, self.pCFS3], 10, [])

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
		del self.t1 
		del self.t2
		del self.t3
		del self.t4
		del self.t5
		del self.dealer
		del self.p2dealer
		del self.p3dealer

		del self.xstep3spec
		del self.xstep3p
		del self.xstep3deal

		# 8949-0357-4
		del self.pCFS1
		del self.pCFS2
		del self.pCFS3
		del self.dCFS


	def testXstep(self):
		self.assertEqual(self.xstep3spec.food, 0)
		self.xstep3deal.feed1()
		self.assertEqual(self.xstep3spec.food, 2)
		self.assertEqual(self.xstep3deal.wateringHole, 3)

	def testToDict(self):		
		self.assertEqual(self.p2dealer.toDict(), {"wateringHole": 3, "deck": [], 
			"players": [{"num": 6, "species": 
							[{"food": 3, "body": 4, "population": 5, "traits": ["carnivore", "cooperation"], "fatFood": 0}], 
							"hand": [], "foodbag": 0}, 
						{"num": 5, "species": 
							[{"food": 1, "body": 2, "population": 3, "traits": ["horns"], "fatFood": 0}], 
							"hand": [], "foodbag": 0}]})

	def testRemovePlayer(self):
		self.assertEqual(len(self.dealer.players), 3)
		self.assertTrue(self.p1 in self.dealer.currentlyFeeding)
		self.assertTrue(self.p2 in self.dealer.currentlyFeeding)
		self.assertTrue(self.p3 in self.dealer.currentlyFeeding)
		self.dealer.removePlayerFromTurn(self.p2)
		self.assertEqual(len(self.dealer.players), 3)
		self.assertTrue(self.p1 in self.dealer.currentlyFeeding)
		self.assertFalse(self.p2 in self.dealer.currentlyFeeding)
		self.assertTrue(self.p3 in self.dealer.currentlyFeeding)
		# check exception raise condition

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

	def testExtinctSpecies(self):
		# nothing changes if non-extinct
		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(len(self.p3.hand), 0)
		self.assertEqual(len(self.dealer.deck), 5)
		self.dealer.extinctSpecies(self.p3, 1)
		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(len(self.p3.hand), 0)
		self.assertEqual(len(self.dealer.deck), 5)

		self.assertEqual(self.extinct.population, 0)
		self.assertEqual(len(self.p8.hand), 0)
		self.assertEqual(len(self.p3dealer.deck), 5)
		self.p3dealer.extinctSpecies(self.p8, 1)
		self.assertEqual(len(self.p8.hand), 2)
		self.assertEqual(self.p8.hand, [self.t1, self.t2])
		self.assertEqual(len(self.p3dealer.deck), 3)
		self.assertEqual(self.p3dealer.deck, [self.t3, self.t4, self.t5])

	def testDistributeCards(self):
		self.assertEqual(len(self.p3.hand), 0)
		self.assertEqual(len(self.dealer.deck), 5)
		self.dealer.distributeCards(self.p3, 2)
		self.assertEqual(self.p3.hand, [self.t1, self.t2])
		self.assertEqual(self.dealer.deck, [self.t3, self.t4, self.t5])

		self.assertEqual(len(self.p3.hand), 2)
		self.assertEqual(len(self.dealer.deck), 3)
		self.dealer.distributeCards(self.p3, 2)
		self.assertEqual(self.p3.hand, [self.t1, self.t2, self.t3, self.t4])
		self.assertEqual(self.dealer.deck, [self.t5])

		self.assertEqual(len(self.p3.hand), 4)
		self.assertEqual(len(self.dealer.deck), 1)
		self.dealer.distributeCards(self.p3, 2)
		self.assertEqual(self.p3.hand, [self.t1, self.t2, self.t3, self.t4, self.t5])
		self.assertEqual(self.dealer.deck, [])

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

	def testCoopForgScavenge(self):
		# cooperation + foraging + scavenging
		# 8949-0357-4
		self.dCFS.feed1()
		self.assertEqual(self.pCFS1.species[0].food, 5)
		self.assertEqual(self.pCFS1.species[1].food, 4)
		self.assertEqual(self.pCFS2.species[0].population, 2)
		self.assertEqual(self.pCFS2.species[0].food, 2)
		self.assertEqual(self.pCFS3.species, [])
		self.assertEqual(self.dCFS.wateringHole, 6)


if __name__ == "__main__":
	unittest.main()
