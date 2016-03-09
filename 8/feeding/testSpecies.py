import unittest
import constants
from jsonParsing import *

class TestSpecies(unittest.TestCase):
    def setUp(self):        
        self.someTraits = [TraitCard("carnivore", 3), TraitCard("ambush", 1)]
        self.defaultSpecies = Species(0, 0, 0, [], 0)

        self.aSpecies = Species(3, 3, 5, self.someTraits, 0)
        self.anotherSpecies = Species(2, 5, 7, self.someTraits, 0)
        self.yetAnotherSpecies = Species(1, 5, 7, self.someTraits, 0)
        self.yetAnotherYetAnotherSpecies = Species(2, 5, 7, self.someTraits, 0)

    def tearDown(self):
        del self.someTraits 
        del self.defaultSpecies 
        del self.aSpecies 
        del self.anotherSpecies 
        del self.yetAnotherSpecies 
        del self.yetAnotherYetAnotherSpecies 

    def testComparators(self):
        self.assertTrue(self.aSpecies.isLarger(False))
        self.assertTrue(self.anotherSpecies.isLarger(self.aSpecies))
        self.assertFalse(self.yetAnotherSpecies.isLarger(self.anotherSpecies))
#        self.assertFalse(yetAnotherYetAnotherSpecies.isLarger(anotherSpecies))

if __name__ == "__main__":
    unittest.main()
