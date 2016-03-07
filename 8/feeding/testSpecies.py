import unittest
import constants


HW_5_TEST_PATH = "homework_5_tests/"

class TestSpecies(unittest.TestCase):
    def testGetSets(self):
        someTraits = [TraitCard(constants.CARNIVORE, 3), TraitCard(constants.AMBUSH, 1)]
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

    def testComparators(self):
        self.assertTrue(aSpecies.isLarger(False))
        self.assertTrue(anotherSpecies.isLarger(aSpecies))
        self.assertFalse(yetAnotherSpecies.isLarger(anotherSpecies))
#        self.assertFalse(yetAnotherYetAnotherSpecies.isLarger(anotherSpecies))


    def testIsAttackable(self):
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
                    with open(HW_5_TEST_PATH + outFiles[i], 'r') as output:
                        input = json.load(input)
                        output = json.load(output)
                        defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(input)
                        self.assertEqual(Species.isAttackable(defend, attack, lNeighbor, rNeighbor), output)

if __name__ == "__main__":
    unittest.main()
