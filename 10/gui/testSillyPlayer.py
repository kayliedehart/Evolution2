import unittest
import json
from sillyPlayer import *
from playerState import PlayerState
import constants


class TestPlayer(unittest.TestCase):

	def setUp(self):
		self.big = Species(food=5, body=1, population=6, traits=["fat-tissue", "carnivore"], fatFood=0)
		self.aCarnivore = Species(food=1, body=2, population=4, traits=["carnivore"], fatFood=0)
		self.fedVeg = Species(food=3, body=4, population=3, traits=[], fatFood=0)
		self.smallerVeg = Species(food=1, body=4, population=2, traits=[], fatFood=0)
		self.smallerFatTissue = Species(food=0, body=4, population=2, traits=["fat-tissue"], fatFood=0)
		# TODO: should food = 2 here, or 0?
		self.fedFatTissue = Species(food=0, body=3, population=2, traits=["fat-tissue"], fatFood=3)
		self.ourSpecies = [self.big, self.aCarnivore, self.fedVeg, self.smallerVeg, self.smallerFatTissue]
		self.ourIndexedSpecies = [(0, self.big), (1, self.aCarnivore), (2, self.fedVeg), (3, self.smallerVeg), (4, self.smallerFatTissue)]
		self.noFatTissue = [self.aCarnivore, self.fedVeg, self.smallerVeg]
		self.noFatTissueIndexed = [(0, self.aCarnivore), (1, self.fedVeg), (2, self.smallerVeg)]
		self.noVeg = [self.big, self.aCarnivore]
		self.noVegIndexed = [(0, self.big), (1, self.aCarnivore)]
		self.aPlayerState = PlayerState(1, 0, self.ourSpecies, [])
		self.big_json = self.big.speciesToJson()
		self.aCarnivore_json = self.aCarnivore.speciesToJson()
		self.fedVeg_json = self.fedVeg.speciesToJson()
		self.smallerVeg_json = self.smallerVeg.speciesToJson()        
		self.bPlayerState = PlayerState.playerStateFromJson([["id", 2],
						 ["species", [self.aCarnivore_json, self.fedVeg_json, self.smallerVeg_json]],
						 ["bag", 0]])
		self.cPlayerState = PlayerState.playerStateFromJson([["id", 3],
						 ["species", [self.big_json, self.aCarnivore_json]],
						 ["bag", 0]])

	def tearDown(self):
		del self.big
		del self.aCarnivore
		del self.fedVeg
		del self.smallerVeg
		del self.smallerFatTissue
		del self.fedFatTissue
		del self.ourSpecies
		del self.ourIndexedSpecies
		del self.noFatTissue
		del self.noFatTissueIndexed
		del self.noVeg
		del self.noVegIndexed
		del self.aPlayerState
		del self.big_json
		del self.aCarnivore_json
		del self.fedVeg_json
		del self.smallerVeg_json
		del self.bPlayerState
		del self.cPlayerState

	def test0067_6(self):
		p1 = PlayerState(1, 0, [Species(0, 1, 1, ["carnivore"], 0), Species(1, 1, 1, ["horns", "cooperation"], 0), Species(1, 1, 1, [], 0)], [])
		p2 = PlayerState(2, 0, [Species(0, 1, 1, [], 0)], [])
		p3 = PlayerState(3, 0, [Species(0, 1, 1, ["cooperation", "scavenger", "climbing"], 0), Species(0, 1, 2, ["scavenger", "cooperation", "climbing"], 0), Species(0, 1, 4, ["foraging", "climbing"], 0)], [])
		self.assertEqual(SillyPlayer.feed(p1, 10, [p1, p2, p3]), [0, 1, 0])
	
	
	def testSortSpecies(self):
		self.ourIndexedSpecies = [(0, self.aCarnivore), (1, self.smallerFatTissue), (2, self.big), (3, self.fedVeg), (4, self.smallerVeg), (5, self.fedFatTissue)]
		unfedSortedSpecies = [(2, self.big), (0, self.aCarnivore), (4, self.smallerVeg), (1, self.smallerFatTissue), (5, self.fedFatTissue)]

		self.assertEqual(SillyPlayer.sortSpecies(self.ourIndexedSpecies), unfedSortedSpecies)

	def testGetFatTissueSpecies(self):
		self.assertEqual(SillyPlayer.getFatTissueSpecies(self.ourIndexedSpecies, 5), (4, 4))
		self.assertEqual(SillyPlayer.getFatTissueSpecies(self.ourIndexedSpecies, 3), (4, 3))
		self.assertEqual(SillyPlayer.getFatTissueSpecies(self.noFatTissueIndexed, 5), (False, 0))

	def testGetVegetarian(self):
		self.assertEqual(SillyPlayer.getVegetarian(self.ourIndexedSpecies), 3)
		self.assertEqual(SillyPlayer.getVegetarian(self.noVegIndexed), False)

	def testGetCarnivoreAttack(self):
		carn, play, prey = SillyPlayer.getCarnivoreAttack(self.ourIndexedSpecies, otherPlayers=[self.bPlayerState, self.cPlayerState])
		self.assertEqual(carn, 0)
		self.assertEqual(play, 1)
		self.assertEqual(prey, 0)
		carn, play, prey = SillyPlayer.getCarnivoreAttack(self.ourIndexedSpecies, otherPlayers=[self.bPlayerState])
		self.assertEqual(carn, 0)
		self.assertEqual(play, 0)
		self.assertEqual(prey, 0)
		carn, play, prey = SillyPlayer.getCarnivoreAttack(self.ourIndexedSpecies, 
			otherPlayers=[PlayerState(4, 0, [Species(1, 1, 1, ["warning-call"], 0), Species(1, 1, 1, ["warning-call"], 0)], [])])
		self.assertFalse(carn)
		self.assertFalse(play)
		self.assertFalse(prey)

	def testFeed(self):
		self.assertEqual(SillyPlayer.feed(self.aPlayerState, 5, [self.bPlayerState, self.cPlayerState]), [4, 4])
		self.assertEqual(SillyPlayer.feed(self.aPlayerState, 1, [self.bPlayerState, self.cPlayerState]), [4, 1])
		self.assertEqual(SillyPlayer.feed(PlayerState(1, 0, [Species(0, 1, 2, [], 0)], []), 5, [self.bPlayerState, self.cPlayerState]), 0)
		self.assertEqual(SillyPlayer.feed(PlayerState(1, 0, [Species(0, 1, 2, ["fat-tissue", "carnivore"], 1), 
																	Species(0, 1, 2, [], 0)], []), 5, [self.bPlayerState, self.cPlayerState]), 1)
		# TODO: should the vegetarian fat-tissue haver be fed?
		self.assertEqual(SillyPlayer.feed(PlayerState(1, 0, [Species(0, 1, 2, ["fat-tissue"], 1), 
																	Species(0, 1, 2, [], 0)], []), 5, [self.bPlayerState, self.cPlayerState]), 0)
		self.assertEqual(SillyPlayer.feed(PlayerState(1, 0, [self.aCarnivore], []), 5, [self.bPlayerState, self.cPlayerState]), [0, 1, 0])
		self.assertEqual(SillyPlayer.feed(PlayerState(1, 0, [self.fedVeg, self.aCarnivore], []), 5, [self.bPlayerState]), [1, 0, 0])



if __name__ == "__main__":
	unittest.main()
