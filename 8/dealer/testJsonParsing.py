import unittest
import constants
from jsonParsing import *
from species import Species
from traitCard import TraitCard
from playerState import PlayerState

class testJsonParsing(unittest.TestCase):

	def setUp(self):
		self.species1J = [["food", 3],
					["body", 4],
					["population", 5],
					["traits", ["carnivore"]]]
		self.species1 = Species(3, 4, 5, ["carnivore"], 0)
		self.species2J = [["food", 1],
					["body", 3],
					["population", 4],
					["traits", ["warning-call", "fat-tissue"]],
					["fat-food", 1]]
		self.species2 = Species(1, 3, 4, ["warning-call", "fat-tissue"], 1)

		self.avgSpeciesJ = [["food", 3],
					   ["body", 4],
					   ["population", 5],
					   ["traits", ["carnivore"]]]
		self.avgSpecies = Species(3, 4, 5, ["carnivore"], 0)

		self.fatTissueSpeciesJ = [["food", 1],
							 ["body", 3],
							 ["population", 4],
							 ["traits", ["warning-call", "fat-tissue"]],
							 ["fat-food", 1]]
		self.fatTissueSpecies = Species(1, 3, 4, ["warning-call", "fat-tissue"], 1)

		self.fatTraitNoFoodJ = [["food", 1],
							["body", 3],
							["population", 4],
							["traits", ["warning-call", "fat-tissue"]]]
		self.fatTraitNoFood = Species(1, 3, 4, ["warning-call", "fat-tissue"], 0)		

		self.onePlayerJ = [["id", 1],
					 ["species", [self.species1J, self.species2J]],
					 ["bag", 0]]
		self.onePlayer = PlayerState(1, 0, [self.species1, self.species2], [])

		self.twoPlayerJ = [["id", 2],
						   ["species", [self.avgSpeciesJ, self.fatTissueSpeciesJ]],
						   ["bag", 0]]
		self.twoPlayer = PlayerState(2, 0, [self.avgSpecies, self.fatTissueSpecies], [])

		self.threePlayerJ = [["id", 3],
							 ["species", [self.fatTraitNoFoodJ]],
							 ["bag", 0]]
		self.threePlayer = PlayerState(3, 0, [self.fatTraitNoFood], [])

	def tearDown(self):
		del self.species1J
		del self.species1
		del self.species2J
		del self.species2
		del self.avgSpeciesJ
		del self.avgSpecies
		del self.fatTissueSpeciesJ
		del self.fatTissueSpecies
		del self.fatTraitNoFoodJ
		del self.fatTraitNoFood
		del self.onePlayerJ
		del self.onePlayer
		del self.twoPlayerJ
		del self.twoPlayer
		del self.threePlayerJ
		del self.threePlayer

	def testSpeciesParsing(self):        
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


		self.assertEqual(JsonParsing.speciesFromJson(self.avgSpeciesJ), self.avgSpecies)
		self.assertEqual(JsonParsing.speciesToJson(self.avgSpecies), self.avgSpeciesJ)

		self.assertEqual(JsonParsing.speciesFromJson(self.fatTissueSpeciesJ), self.fatTissueSpecies)
		self.assertEqual(JsonParsing.speciesToJson(self.fatTissueSpecies), self.fatTissueSpeciesJ)

		self.assertEqual(JsonParsing.speciesFromJson(self.fatTraitNoFoodJ), self.fatTraitNoFood)
		self.assertEqual(JsonParsing.speciesToJson(self.fatTraitNoFood), self.fatTraitNoFoodJ)

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
		self.assertEqual(JsonParsing.playerStateFromJson(self.onePlayerJ), self.onePlayer)
		self.assertEqual(JsonParsing.playerStateToJson(self.onePlayer), self.onePlayerJ)
		self.assertEqual(JsonParsing.playerStateFromJson(self.twoPlayerJ), self.twoPlayer)
		self.assertEqual(JsonParsing.playerStateToJson(self.twoPlayer), self.twoPlayerJ)

	def testDealerParsing(self):
		config = [[self.onePlayerJ, self.twoPlayerJ, self.threePlayerJ], 5, []]
		deal = Dealer([self.onePlayer, self.twoPlayer, self.threePlayer], 5, [])

		self.assertEqual(JsonParsing.dealerFromJson(config), deal)
		self.assertEqual(JsonParsing.dealerToJson(deal), config)

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
