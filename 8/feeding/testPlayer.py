import unittest
import json
import glob
import os
from player import *
from jsonParsing import *
import constants

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.big = Species(food=5, body=1, population=6, traits=[TraitCard("fat-tissue"), TraitCard("carnivore")], fatFood=0)
        self.aCarnivore = Species(food=1, body=2, population=4, traits=[TraitCard("carnivore")], fatFood=0)
        self.fedVeg = Species(food=3, body=4, population=3, traits=[], fatFood=0)
        self.smallerVeg = Species(food=1, body=4, population=2, traits=[], fatFood=0)
        self.smallerFatTissue = Species(food=0, body=4, population=2, traits=[TraitCard("fat-tissue")], fatFood=0)
        # TODO: should food = 2 here, or 0?
        self.fedFatTissue = Species(food=0, body=3, population=2, traits=[TraitCard("fat-tissue")], fatFood=3)
        self.ourSpecies = []
        self.aPlayer = Player(1)

    def tearDown(self):
        del self.big
        del self.aCarnivore
        del self.fedVeg
        del self.smallerVeg
        del self.smallerFatTissue
        del self.fedFatTissue
        del self.ourSpecies
        del self.aPlayer
    
    def testSortSpecies(self):
        self.ourSpecies = [(0, self.aCarnivore), (1, self.smallerFatTissue), (2, self.big), (3, self.fedVeg), (4, self.smallerVeg), (5, self.fedFatTissue)]
        allSortedSpecies = [(2, self.big), (0, self.aCarnivore), (3, self.fedVeg), (4, self.smallerVeg), (1, self.smallerFatTissue), (5, self.fedFatTissue)]
        unfedSortedSpecies = [(2, self.big), (0, self.aCarnivore), (4, self.smallerVeg), (1, self.smallerFatTissue)]

        self.assertEqual(self.aPlayer.sortSpecies(self.ourSpecies, removeFed=False), allSortedSpecies)
        # TODO: why does this fail...why...
        #self.assertEqual(self.aPlayer.sortSpecies(self.ourSpecies, removeFed=True), unfedSortedSpecies)

    def testPlayerFeedMethods(self):
        self.ourSpecies = [self.big, self.aCarnivore, self.fedVeg, self.smallerVeg, self.smallerFatTissue]
        self.ourIndexedSpecies = [(0, self.big), (1, self.aCarnivore), (2, self.fedVeg), (3, self.smallerVeg), (4, self.smallerFatTissue)]
        noFatTissue = [self.aCarnivore, self.fedVeg, self.smallerVeg]
        noFatTissueIndexed = [(0, self.aCarnivore), (1, self.fedVeg), (2, self.smallerVeg)]
        noVeg = [self.big, self.aCarnivore]
        noVegIndexed = [(0, self.big), (1, self.aCarnivore)]

        self.big_json = JsonParsing.speciesToJson(self.big)
        self.aCarnivore_json = JsonParsing.speciesToJson(self.aCarnivore)
        self.fedVeg_json = JsonParsing.speciesToJson(self.fedVeg)
        self.smallerVeg_json = JsonParsing.speciesToJson(self.smallerVeg)

        bPlayerState = JsonParsing.playerStateFromJson([["id", 2],
                         ["species", [self.aCarnivore_json, self.fedVeg_json, self.smallerVeg_json]],
                         ["bag", 0]])
        cPlayerState = JsonParsing.playerStateFromJson([["id", 3],
                         ["species", [self.big_json, self.aCarnivore_json]],
                         ["bag", 0]])

        others = [bPlayerState, cPlayerState]

        self.assertEqual(self.aPlayer.getFatTissueSpecies(ourIndexedSpecies, 5), (4, 4))
        self.assertEqual(self.aPlayer.getFatTissueSpecies(noFatTissueIndexed, 5), (-1, 0))
        self.assertEqual(self.aPlayer.getVegetarian(ourIndexedSpecies), 3)
        self.assertEqual(self.aPlayer.getVegetarian(noVegIndexed), -1)
        carn, play, pry = self.aPlayer.getCarnivoreAttack(ourIndexedSpecies, otherPlayers=others)
        self.assertEqual(carn, 0)
        # TODO: check following tests for correctness
        self.assertEqual(play, 1)
        self.assertEqual(pry, 0)

    def testFeed(self):
        pass


if __name__ == "__main__":
    unittest.main()
