import unittest
import json
from species import *
sys.path.append('../../6/feeding')
from player import *
from feedingAction import *
from playerState import *


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
        self.assertTrue(anotherSpecies.isLarger(yetAnotherSpecies))
        self.assertTrue(anotherSpecies.isLarger(yetAnotherYetAnotherSpecies))

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
        
        with open('json_tests/burrowing_false.json', 'r') as jsonObj:
            burrowing_false = json.load(jsonObj)

        with open('json_tests/burrowing_true.json', 'r') as jsonObj:
            burrowing_true = json.load(jsonObj)

        with open('json_tests/carnivore_false.json', 'r') as jsonObj:
            carnivore_false = json.load(jsonObj)

        with open('json_tests/climbing_false.json', 'r') as jsonObj:
            climbing_false = json.load(jsonObj)

        with open('json_tests/climbing_true.json', 'r') as jsonObj:
            climbing_true = json.load(jsonObj)

        with open('json_tests/hard_shell_false.json', 'r') as jsonObj:
            hard_shell_false = json.load(jsonObj)

        with open('json_tests/hard_shell_pack_hunting_false.json', 'r') as jsonObj:
            hard_shell_pack_hunting_false = json.load(jsonObj)

        with open('json_tests/hard_shell_pack_hunting_true.json', 'r') as jsonObj:
            hard_shell_pack_hunting_true = json.load(jsonObj)

        with open('json_tests/hard_shell_true.json', 'r') as jsonObj:
            hard_shell_true = json.load(jsonObj)

        with open('json_tests/herding_false.json', 'r') as jsonObj:
            herding_false = json.load(jsonObj)

        with open('json_tests/herding_horns_false.json', 'r') as jsonObj:
            herding_horns_false = json.load(jsonObj)

        with open('json_tests/herding_horns_true.json', 'r') as jsonObj:
            herding_horns_true = json.load(jsonObj)

        with open('json_tests/herding_true.json', 'r') as jsonObj:
            herding_true = json.load(jsonObj)

        with open('json_tests/symbiosis_false.json', 'r') as jsonObj:
            symbiosis_false = json.load(jsonObj)

        with open('json_tests/symbiosis_true.json', 'r') as jsonObj:
            symbiosis_true = json.load(jsonObj)

        with open('json_tests/warning-call_ambush_true.json', 'r') as jsonObj:
            warning_call_ambush_true = json.load(jsonObj)

        with open('json_tests/warning-call_noambush_false.json', 'r') as jsonObj:
            warning_call_noambush_false = json.load(jsonObj)

        self.assertFalse(Species.isAttackable(burrowing_false))
        self.assertTrue(Species.isAttackable(burrowing_true))
        self.assertFalse(Species.isAttackable(carnivore_false))
        self.assertTrue(Species.isAttackable(climbing_true))
        self.assertFalse(Species.isAttackable(climbing_false))
        self.assertFalse(Species.isAttackable(hard_shell_false))
        self.assertFalse(Species.isAttackable(hard_shell_pack_hunting_false))
        self.assertTrue(Species.isAttackable(hard_shell_pack_hunting_true))
        self.assertTrue(Species.isAttackable(hard_shell_true))
        self.assertFalse(Species.isAttackable(herding_false))
        self.assertFalse(Species.isAttackable(herding_horns_false))
        self.assertTrue(Species.isAttackable(herding_horns_true))
        self.assertTrue(Species.isAttackable(herding_true))
        self.assertFalse(Species.isAttackable(symbiosis_false))
        self.assertTrue(Species.isAttackable(symbiosis_true))
        self.assertTrue(Species.isAttackable(warning_call_ambush_true))
        self.assertFalse(Species.isAttackable(warning_call_noambush_false))

    def testPlayerState(self):
        species1 = [["food", 3],
                    ["body", 4],
                    ["population", 5],
                    ["traits", ["carnivore"]]]
        species2 = [["food", 1],
                    ["body", 3],
                    ["population", 4],
                    ["traits", ["vegetarian", "warning-call"]]]

        onePlayer = [["id", 1],
                    ["species", [species1, species2]],
                    ["bag", 0]]

        ps = PlayerState(onePlayer)
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
        big = Species(food=5, body=1, population=6, traits=["fat-tissue"], fatFood=0)
        aCarnivore = Species(food=1, body=2, population=4, traits=["carnivore"])
        fedVeg = Species(food=3, body=4, population=3, traits=["vegetarian"])
        smallerVeg = Species(food=1, body=4, population=2, traits=["vegetarian"])
        smallerFatTissue = Species(food=0, body=4, population=2, traits=["fat-tissue"])

        ourSpecies = [big, aCarnivore, fedVeg, smallerVeg, smallerFatTissue]
        noFatTissue = [aCarnivore, fedVeg, smallerVeg]
        noVeg = [big, aCarnivore, smallerFatTissue]

        big_json = big.toJsonArray()
        aCarnivore_json = aCarnivore.toJsonArray()
        fedVeg_json = fedVeg.toJsonArray()
        smallerVeg_json = smallerVeg.toJsonArray()
        smallerFatTissue_json = smallerFatTissue.toJsonArray()

        aPlayer = Player(1)
        bPlayerState = PlayerState([["id", 2],
                         ["species", [aCarnivore_json, fedVeg_json, smallerVeg_json]],
                         ["bag", 0]])
        cPlayerState = PlayerState([["id", 3],
                         ["species", [big_json, aCarnivore_json, smallerFatTissue_json]],
                         ["bag", 0]])

        others = [bPlayerState, cPlayerState]

        self.assertEqual(aPlayer.getFatTissueSpecies(ourSpecies), (smallerFatTissue, 4))
        self.assertEqual(aPlayer.getFatTissueSpecies(noFatTissue), (False, 0))
        self.assertEqual(aPlayer.getVegetarian(ourSpecies), smallerVeg)
        self.assertEqual(aPlayer.getVegetarian(noVeg), False)
        carn, play, pry = aPlayer.getCarnivoreAttack(ourSpecies, otherPlayers=others)
        self.assertEqual(carn.toJsonArray(), (aCarnivore, cPlayerState, big))
