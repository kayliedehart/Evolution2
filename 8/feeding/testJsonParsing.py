import unittest
import constants
from jsonParsing import *
from species import Species
from traitCard import TraitCard
from playerState import PlayerState

class testJsonParsing(unittest.TestCase):

	def testSpeciesParsing(self):        
		avgSpeciesJ = [["food", 3],
					   ["body", 4],
					   ["population", 5],
					   ["traits", ["carnivore"]]]
		avgSpecies = Species(3, 4, 5, ["carnivore"], 0)

		fatTissueSpeciesJ = [["food", 1],
							 ["body", 3],
							 ["population", 4],
							 ["traits", ["warning-call", "fat-tissue"]],
							 ["fat-food", 1]]
		fatTissueSpecies = Species(1, 3, 4, ["warning-call", "fat-tissue"], 1)

		fatTraitNoFoodJ = [["food", 1],
							["body", 3],
							["population", 4],
							["traits", ["warning-call", "fat-tissue"]]]
		fatTraitNoFood = Species(1, 3, 4, ["warning-call", "fat-tissue"], 0)

		invalidJ = ["no"]

		validButWrongJ = [["wrong thing", 3],
						  ["another wrong thing", 4],
						  ["yawt", 5],
						  ["yayawt", ["carnivore"]]]

		fatFoodNoTraitJ = [["food", 1],
						  ["body", 3],
						  ["population", 4],
						  ["traits", ["warning-call"]],
						  ["fat-food", 1]]

		optJ = False


		self.assertEqual(JsonParsing.speciesFromJson(avgSpeciesJ), avgSpecies)
		self.assertEqual(JsonParsing.speciesToJson(avgSpecies), avgSpeciesJ)

		self.assertEqual(JsonParsing.speciesFromJson(fatTissueSpeciesJ), fatTissueSpecies)
		self.assertEqual(JsonParsing.speciesToJson(fatTissueSpecies), fatTissueSpeciesJ)

		self.assertEqual(JsonParsing.speciesFromJson(fatTraitNoFoodJ), fatTraitNoFood)
		self.assertEqual(JsonParsing.speciesToJson(fatTraitNoFood), fatTraitNoFoodJ)

		self.assertEqual(JsonParsing.speciesFromJson(optJ), False)
		self.assertEqual(JsonParsing.speciesToJson(False), optJ)

		# TODO: catch exceptions for tests
#        self.assertEqual(JsonParsing.speciesFromJson(invalidJ), )
#        self.assertEqual(JsonParsing.speciesFromJson(validButWrongJ), )
#        self.assertEqual(JsonParsing.speciesFromJson(fatFoodNoTraitJ), )
#        with self.assertRaises ValueError:
#            the test case that fails

	
	def testSituationParsing(self):
		situation1J = [[["food", 1], ["body", 0], ["population", 1], ["traits", []]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", ["carnivore"]]],
					  False,
					  False]
		situation1 = (Species(1, 0, 1, [], 0), Species(1, 0, 1, ["carnivore"], 0), Species(0, 0, 0, [], 0), Species(0, 0, 0, [], 0))

		situation2J = [[["food", 1], ["body", 0], ["population", 1], ["traits", []]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", ["carnivore"]]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", []]],
					  False]
		situation2 = (Species(1, 0, 1, [], 0), Species(1, 0, 1, ["carnivore"], 0), Species(1, 0, 1, [], 0), Species(0, 0, 0, [], 0))

		situation3J = [[["food", 1], ["body", 0], ["population", 1], ["traits", []]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", ["carnivore"]]],
					  False,
					  [["food", 1], ["body", 0], ["population", 1], ["traits", []]]]
		situation3 = (Species(1, 0, 1, [], 0), Species(1, 0, 1, ["carnivore"], 0), Species(0, 0, 0, [], 0), Species(1, 0, 1, [], 0))

		situation4J = [[["food", 1], ["body", 0], ["population", 1], ["traits", []]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", ["carnivore"]]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", []]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", []]]]
		situation4 = (Species(1, 0, 1, [], 0), Species(1, 0, 1, ["carnivore"], 0), Species(1, 0, 1, [], 0), Species(1, 0, 1, [], 0))

		badSituation1 = [False, False, [["food", 1], ["body", 0], ["population", 1], ["traits", []]], False]

		self.assertEqual(JsonParsing.situationFromJson(situation1J), situation1)
		self.assertEqual(JsonParsing.situationFromJson(situation2J), situation2)
		self.assertEqual(JsonParsing.situationFromJson(situation3J), situation3)
		self.assertEqual(JsonParsing.situationFromJson(situation4J), situation4)
		# TODO: check for exiting
#        self.assertEqual(JsonParsing.situationFromJson(badSituation1), )


	def testPlayerStateParsing(self):
		species1J = [["food", 3],
					["body", 4],
					["population", 5],
					["traits", ["carnivore"]]]
		species1 = Species(3, 4, 5, ["carnivore"], 0)
		species2J = [["food", 1],
					["body", 3],
					["population", 4],
					["traits", ["warning-call", "fat-tissue"]],
					["fat-food", 1]]
		species2 = Species(1, 3, 4, ["warning-call", "fat-tissue"], 1)

		onePlayerJ = [["id", 1],
					 ["species", [species1J, species2J]],
					 ["bag", 0]]
		onePlayer = PlayerState(1, 0, [species1, species2], [])

		self.assertEqual(JsonParsing.playerStateFromJson(onePlayerJ), onePlayer)
		self.assertEqual(JsonParsing.playerStateToJson(onePlayer), onePlayerJ)


	def testCheckTrait(self):
		goodTrait = "fat-tissue"
		carn = "carnivore"
		warn = "warning-call"
		badTrait = "invincibility"

		self.assertTrue(JsonParsing.checkTrait(goodTrait))
		self.assertTrue(JsonParsing.checkTrait(carn))
		self.assertTrue(JsonParsing.checkTrait(warn))
		
		self.assertFalse(JsonParsing.checkTrait(badTrait))



if __name__ == "__main__":
	unittest.main()
