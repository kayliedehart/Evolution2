import unittest
import json
import glob
import os
from player import *
import constants

HW_6_TEST_PATH = "homework_6_tests/"

class TestPlayer(unittest.TestCase):
    
    def testFeed(self):
        os.chdir(HW_6_TEST_PATH)
        inFiles = glob.glob("*-in.json")
        outFiles = glob.glob("*-out.json")
        # Loop through the files in homework_6_tests directory and make sure inputs match expected outputs
        for i in range(len(inFiles)):
            inFileName = inFiles[i].replace("-in.json", "")
            outFileName = outFiles[i].replace("-out.json", "")
            # Make sure that these are the same corresponding test files
            self.assertEquals(inFileName, outFileName)
            if inFileName == outFileName:
                with open(inFiles[i], 'r') as input:
                    with open(outFiles[i], 'r') as output:
                        if os.stat(outFiles[i]).st_size > 0:
                            output = json.load(output)
                        else:
                            output = False
                        input = json.load(input)
                        ps = PlayerState.convertPlayerState(input[0])
                        wateringHole = int(input[1])
                        otherPlayers = []
                        for player in input[2]:
                            if player:
                                otherPlayers.append(PlayerState.convertPlayerState(player))
                        player = Player(ps.num)
                        self.assertEqual(player.feed(ps, wateringHole, otherPlayers), output)
        os.chdir("..")


    def testPlayerFeedMethods(self):
        big = Species(food=5, body=1, population=6, traits=[TraitCard(constants.FAT_TISSUE), TraitCard(constants.CARNIVORE)], fatFood=0)
        aCarnivore = Species(food=1, body=2, population=4, traits=[TraitCard(constants.CARNIVORE)])
        fedVeg = Species(food=3, body=4, population=3, traits=[])
        smallerVeg = Species(food=1, body=4, population=2, traits=[])
        smallerFatTissue = Species(food=0, body=4, population=2, traits=[TraitCard(constants.FAT_TISSUE)])

        ourSpecies = [big, aCarnivore, fedVeg, smallerVeg, smallerFatTissue]
        ourIndexedSpecies = [(0, big), (1, aCarnivore), (2, fedVeg), (3, smallerVeg), (4, smallerFatTissue)]
        noFatTissue = [aCarnivore, fedVeg, smallerVeg]
        noFatTissueIndexed = [(0, aCarnivore), (1, fedVeg), (2, smallerVeg)]
        noVeg = [big, aCarnivore]
        noVegIndexed = [(0, big), (1, aCarnivore)]

        big_json = big.toJsonArray()
        aCarnivore_json = aCarnivore.toJsonArray()
        fedVeg_json = fedVeg.toJsonArray()
        smallerVeg_json = smallerVeg.toJsonArray()

        aPlayer = Player(1)
        bPlayerState = PlayerState.convertPlayerState([["id", 2],
                         ["species", [aCarnivore_json, fedVeg_json, smallerVeg_json]],
                         ["bag", 0]])
        cPlayerState = PlayerState.convertPlayerState([["id", 3],
                         ["species", [big_json, aCarnivore_json]],
                         ["bag", 0]])

        others = [bPlayerState, cPlayerState]

        self.assertEqual(aPlayer.getFatTissueSpecies(ourIndexedSpecies, 5), (4, 4))
        self.assertEqual(aPlayer.getFatTissueSpecies(noFatTissueIndexed, 5), (-1, 0))
        self.assertEqual(aPlayer.getVegetarian(ourIndexedSpecies), 3)
        self.assertEqual(aPlayer.getVegetarian(noVegIndexed), -1)
        carn, play, pry = aPlayer.getCarnivoreAttack(ourIndexedSpecies, otherPlayers=others)
        self.assertEqual(carn, 0)
        # TODO: check following tests for correctness
        self.assertEqual(play, 1)
        self.assertEqual(pry, 0)

if __name__ == "__main__":
    unittest.main()
