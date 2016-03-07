import unittest
import constants
from jsonParsing import *
from species import Species
from traitCard import TraitCard

class testJsonParsing(unittest.TestCase):

    def testSpeciesParsing(self):
        avgSpeciesJ = [["food", 3],
                        ["body", 4],
                        ["population", 5],
                        ["traits", ["carnivore"]]]
        avgSpecies = Species(3, 4, 5, [TraitCard(constants.CARNIVORE)])

        fatTissueSpeciesJ = [["food", 1],
                             ["body", 3],
                             ["population", 4],
                             ["traits", ["warning-call", "fat-tissue"]],
                             ["fat-food", 1]]
        fatTissueSpecies = Species(1, 3, 4, [TraitCard(constants.WARNING_CALL), TraitCard(constants.FAT_TISSUE)], 1)

        fatTraitNoFoodJ = [["food", 1],
                            ["body", 3],
                            ["population", 4],
                            ["traits", ["warning-call", "fat-tissue"]]]
        fatTraitNoFood = Species(1, 3, 4, [TraitCard(constants.WARNING_CALL), TraitCard(constants.FAT_TISSUE)])

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


"""
def testPlayerStateParsing(self):
    species1 = [["food", 3],
    ["body", 4],
    ["population", 5],
    ["traits", ["carnivore"]]]

    onePlayer = [["id", 1],
    ["species", [species1, species2]],
    ["bag", 0]]

    ps = PlayerState.convertPlayerState(onePlayer)
    self.assertEqual(ps.num, onePlayer[0][1])
    self.assertEqual(ps.foodbag, onePlayer[2][1])
    self.assertEqual(ps.traits, [])
    """


if __name__ == "__main__":
    unittest.main()
