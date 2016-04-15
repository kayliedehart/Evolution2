import unittest
import constants
from species import *
from traitCard import *
from playerState import *
from dealer import *

class testJsonParsing(unittest.TestCase):

	def setUp(self):
		self.species1J = [["food", 3],
					["body", 4],
					["population", 5],
					["traits", ["carnivore"]]]
		self.species1 = Species(3, 4, 5, [TraitCard("carnivore")], 0)
		self.species2J = [["food", 1],
					["body", 3],
					["population", 4],
					["traits", ["warning-call", "fat-tissue"]],
					["fat-food", 1]]
		self.species2 = Species(1, 3, 4, [TraitCard("warning-call"), TraitCard("fat-tissue")], 1)

		self.avgSpeciesJ = [["food", 3],
					   ["body", 4],
					   ["population", 5],
					   ["traits", ["carnivore"]]]
		self.avgSpecies = Species(3, 4, 5, [TraitCard("carnivore")], 0)

		self.fatTissueSpeciesJ = [["food", 1],
							 ["body", 3],
							 ["population", 4],
							 ["traits", ["warning-call", "fat-tissue"]],
							 ["fat-food", 1]]
		self.fatTissueSpecies = Species(1, 3, 4, [TraitCard("warning-call"), TraitCard("fat-tissue")], 1)

		self.fatTraitNoFoodJ = [["food", 1],
							["body", 3],
							["population", 4],
							["traits", ["warning-call", "fat-tissue"]]]
		self.fatTraitNoFood = Species(1, 3, 4, [TraitCard("warning-call"), TraitCard("fat-tissue")], 0)		

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

		self.config = [[self.onePlayerJ, self.twoPlayerJ, self.threePlayerJ], 5, []]
		self.deal = Dealer([self.onePlayer, self.twoPlayer, self.threePlayer], 5, [])

		self.goodTrait = "fat-tissue"
		self.carn = "carnivore"
		self.warn = "warning-call"
		self.badTrait = "invincibility"

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
		del self.config
		del self.deal
		del self.goodTrait
		del self.carn
		del self.warn
		del self.badTrait

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


		self.assertEqual(Species.speciesFromJson(self.avgSpeciesJ), self.avgSpecies)
		self.assertEqual(self.avgSpecies.speciesToJson(), self.avgSpeciesJ)

		self.assertEqual(Species.speciesFromJson(self.fatTissueSpeciesJ), self.fatTissueSpecies)
		self.assertEqual(self.fatTissueSpecies.speciesToJson(), self.fatTissueSpeciesJ)

		self.assertEqual(Species.speciesFromJson(self.fatTraitNoFoodJ), self.fatTraitNoFood)
		self.assertEqual(self.fatTraitNoFood.speciesToJson(), self.fatTraitNoFoodJ)

		self.assertEqual(Species.speciesFromJson(optJ), False)

	
	def testSituationParsing(self):
		situation1J = [[["food", 1], ["body", 0], ["population", 1], ["traits", []]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", ["carnivore"]]],
					  False,
					  False]
		situation1 = (Species(1, 0, 1, [], 0), Species(1, 0, 1, [TraitCard("carnivore")], 0), False, False)

		situation2J = [[["food", 1], ["body", 0], ["population", 1], ["traits", []]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", ["carnivore"]]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", []]],
					  False]
		situation2 = (Species(1, 0, 1, [], 0), Species(1, 0, 1, [TraitCard("carnivore")], 0), Species(1, 0, 1, [], 0), False)

		situation3J = [[["food", 1], ["body", 0], ["population", 1], ["traits", []]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", ["carnivore"]]],
					  False,
					  [["food", 1], ["body", 0], ["population", 1], ["traits", []]]]
		situation3 = (Species(1, 0, 1, [], 0), Species(1, 0, 1, [TraitCard("carnivore")], 0), False, Species(1, 0, 1, [], 0))

		situation4J = [[["food", 1], ["body", 0], ["population", 1], ["traits", []]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", ["carnivore"]]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", []]],
					  [["food", 1], ["body", 0], ["population", 1], ["traits", []]]]
		situation4 = (Species(1, 0, 1, [], 0), Species(1, 0, 1, [TraitCard("carnivore")], 0), Species(1, 0, 1, [], 0), Species(1, 0, 1, [], 0))

		badSituation1 = [False, False, [["food", 1], ["body", 0], ["population", 1], ["traits", []]], False]

		self.assertEqual(Species.situationFromJson(situation1J), situation1)
		self.assertEqual(Species.situationFromJson(situation2J), situation2)
		self.assertEqual(Species.situationFromJson(situation3J), situation3)
		self.assertEqual(Species.situationFromJson(situation4J), situation4)

	def testPlayerStateParsing(self):
		self.assertEqual(PlayerState.playerStateFromJson(self.onePlayerJ), self.onePlayer)
		self.assertEqual(self.onePlayer.playerStateToJson(), self.onePlayerJ)
		self.assertEqual(PlayerState.playerStateFromJson(self.twoPlayerJ), self.twoPlayer)
		self.assertEqual(self.twoPlayer.playerStateToJson(), self.twoPlayerJ)

	def testDealerParsing(self):
		self.assertEqual(Dealer.dealerFromJson(self.config), self.deal)
		self.assertEqual(self.deal.dealerToJson(), self.config)

	def testCheckTrait(self):
		self.assertTrue(TraitCard.checkTrait(self.goodTrait))
		self.assertTrue(TraitCard.checkTrait(self.carn))
		self.assertTrue(TraitCard.checkTrait(self.warn))
		
		self.assertFalse(TraitCard.checkTrait(self.badTrait))


if __name__ == "__main__":
	unittest.main()
