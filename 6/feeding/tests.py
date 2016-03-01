import unittest
import json
import glob
import os
from player import *
from feedingAction import *
from playerState import *

ATTACK_TEST_PATH = "attack_tests/"
HW_5_TEST_PATH = "homework_5_tests/"
HW_6_TEST_PATH = "homework_6_tests/"
FEED_TEST_PATH = "feed_tests/"

class Tests(unittest.TestCase):
    def testSpeciesMethods(self):
        someTraits = [["carnivore", 3], ["ambush", 1]]
        defaultSpecies = Species()
        defaultSpecies.setBody(3)
        defaultSpecies.setFoodPoints(3)
        defaultSpecies.setTraits(someTraits)

        aSpecies = Species(3, 3, 5, someTraits)
        anotherSpecies = Species(2, 5, 7, someTraits)
        yetAnotherSpecies = Species(1, 5, 7, someTraits)
        yetAnotherYetAnotherSpecies = Species(2, 5, 7, someTraits)

        self.assertEqual(defaultSpecies.body, aSpecies.body)
        self.assertEqual(defaultSpecies.food, aSpecies.food)
        self.assertEqual(defaultSpecies.traits, aSpecies.traits)

        self.assertTrue(aSpecies.isLarger(False))
        self.assertTrue(anotherSpecies.isLarger(aSpecies))
        self.assertFalse(yetAnotherSpecies.isLarger(anotherSpecies))
#        self.assertFalse(yetAnotherYetAnotherSpecies.isLarger(anotherSpecies))

    def testConvertSpecies(self):
        goodJson = [["food", 3],
                    ["body", 4],
                    ["population", 5],
                    ["traits", ["carnivore"]]]
        badJson = [["food", 3],
                   ["nonsense", 4],
                   ["population", 4],
                   ["traits", ["carnivore"]]]

        self.assertFalse(Species.convertSpecies(badJson))
        self.assertFalse(Species.convertSpecies(False))
        self.assertEqual(Species.convertSpecies(goodJson).body, 4)
        self.assertEqual(Species.convertSpecies(goodJson).traits[0], "carnivore")

    def testSpeciesIsAttackable(self):
        
        with open(ATTACK_TEST_PATH + 'burrowing1-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertFalse(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'burrowing2-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertTrue(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'carnivore1-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertFalse(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'climbing1-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertFalse(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'climbing2-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertTrue(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'hard-shell1-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertFalse(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'hard-shell-pack-hunting1-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertFalse(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'hard-shell-pack-hunting2-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertTrue(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'hard-shell2-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertTrue(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'herding1-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertFalse(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'herding-horns1-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertFalse(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'herding-horns2-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertTrue(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'herding2-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertTrue(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'symbiosis1-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertFalse(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'symbiosis2-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertTrue(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'warning-call-ambush1-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertTrue(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        with open(ATTACK_TEST_PATH + 'warning-call-noambush1-in.json', 'r') as jsonObj:
            defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(json.load(jsonObj))
        self.assertFalse(Species.isAttackable(defend, attack, rNeighbor, lNeighbor))

        os.chdir(HW_5_TEST_PATH)
        inFiles = glob.glob("*-in.json")
        outFiles = glob.glob("*-out.json")
        os.chdir("..")
        # Loop through the files in homework_5_tests directory and make sure inputs match expected outputs
        for i in range(len(inFiles)):
            inFileName = inFiles[i].replace("-in.json", "")
            outFileName = outFiles[i].replace("-out.json", "")
            # Make sure that these are the same corresponding test files
            self.assertEquals(inFileName, outFileName)
            if inFileName == outFileName:
                with open(HW_5_TEST_PATH + inFiles[i], 'r') as input:
                    with open(HW_5_TEST_PATH +  outFiles[i], 'r') as output:
                        input = json.load(input)
                        output = json.load(output)
                        defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(input)
                        self.assertEqual(Species.isAttackable(defend, attack, lNeighbor, rNeighbor), output)


        os.chdir(HW_6_TEST_PATH)
        inFiles = glob.glob("*-in.json")
        outFiles = glob.glob("*-out.json")
        os.chdir("..")
        # Loop through the files in homework_6_tests directory and make sure inputs match expected outputs
        for i in range(len(inFiles)):
            inFileName = inFiles[i].replace("-in.json", "")
            outFileName = outFiles[i].replace("-out.json", "")
            # Make sure that these are the same corresponding test files
            self.assertEquals(inFileName, outFileName)
            if inFileName == outFileName:
                with open(HW_6_TEST_PATH + inFiles[i], 'r') as input:
                    with open(HW_6_TEST_PATH + outFiles[i], 'r') as output:
                        input = json.load(input)
                        output = FeedingAction.jsonToFeeding(json.load(output))
                        print inFileName

                        ps = PlayerState.convertPlayerState(input[0])
                        wateringHole = int(input[1])
                        otherPlayers = []
                        for player in input[2]:
                            if player:
                                otherPlayers.append(PlayerState.convertPlayerState(player))
                        player = Player(ps.num)
                        #  TODO: change this to comparing objects. json is so it prints in a comprehensible way
                        self.assertEqual(FeedingAction.toJsonArray(player.feed(ps, wateringHole, otherPlayers)),
                                                                                    FeedingAction.toJsonArray(output))


    def testPlayerState(self):
        species1 = [["food", 3],
                    ["body", 4],
                    ["population", 5],
                    ["traits", ["carnivore"]]]
        species2 = [["food", 1],
                    ["body", 3],
                    ["population", 4],
                    ["traits", ["warning-call"]]]

        onePlayer = [["id", 1],
                    ["species", [species1, species2]],
                    ["bag", 0]]

        ps = PlayerState.convertPlayerState(onePlayer)
        self.assertEqual(ps.num, onePlayer[0][1])
        self.assertEqual(ps.foodbag, onePlayer[2][1])
        self.assertEqual(ps.traits, [])

    def testFeedingAction(self):
        species1 = [["food", 3],
                    ["body", 4],
                    ["population", 5],
                    ["traits", ["vegetarian", "fat-tissue"]]]
        species2 = [["food", 1],
                    ["body", 3],
                    ["population", 4],
                    ["traits", ["vegetarian", "warning-call"]]]
        onePlayer = [["id", 1],
                    ["species", [species2]],
                    ["bag", 0]]


        noMore = FeedingAction.createAction(False)
        fatTissue = FeedingAction.createAction("fat-tissue", callerSpecies=species1, tokens=3)
        vegetarian = FeedingAction.createAction("vegetarian", callerSpecies=species1)
        attack = FeedingAction.createAction("attack", callerSpecies=species1, defender=onePlayer, prey=species2)
        overloaded1 = FeedingAction.createAction(False, tokens=0)
        overloaded2 = FeedingAction.createAction("vegetarian", callerSpecies=species1, defender=onePlayer, prey=species2)

        self.assertEqual(noMore, False)
        self.assertEqual(fatTissue, [species1, 3])
        self.assertEqual(vegetarian, [species1])
        self.assertEqual(attack, [species1, onePlayer, species2])
        self.assertEqual(noMore, overloaded1)
        self.assertEqual(vegetarian, overloaded2)

    def testPlayerFeedMethods(self):
        big = Species(food=5, body=1, population=6, traits=["fat-tissue", "carnivore"], fatFood=0)
        aCarnivore = Species(food=1, body=2, population=4, traits=["carnivore"])
        fedVeg = Species(food=3, body=4, population=3, traits=[])
        smallerVeg = Species(food=1, body=4, population=2, traits=[])
        smallerFatTissue = Species(food=0, body=4, population=2, traits=["fat-tissue"])

        ourSpecies = [big, aCarnivore, fedVeg, smallerVeg, smallerFatTissue]
        noFatTissue = [aCarnivore, fedVeg, smallerVeg]
        noVeg = [big, aCarnivore]

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

        self.assertEqual(aPlayer.getFatTissueSpecies(ourSpecies), (smallerFatTissue, 4))
        self.assertEqual(aPlayer.getFatTissueSpecies(noFatTissue), (False, 0))
        self.assertEqual(aPlayer.getVegetarian(ourSpecies).toJsonArray(), smallerVeg.toJsonArray())
        self.assertEqual(aPlayer.getVegetarian(noVeg), False)
        carn, play, pry = aPlayer.getCarnivoreAttack(ourSpecies, otherPlayers=others)
        self.assertEqual(carn.toJsonArray(), aCarnivore_json)
        # TODO: check following tests for correctness
        self.assertEqual(play.num, 3)
        self.assertEqual(pry.toJsonArray(), big_json)

if __name__ == "__main__":
    unittest.main()
