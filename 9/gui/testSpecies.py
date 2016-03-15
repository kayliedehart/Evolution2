import unittest
import constants
from jsonParsing import *


class TestSpecies(unittest.TestCase):

	def setUp(self):        
		self.someTraits = ["carnivore", "ambush"]
		self.defaultSpecies = Species(0, 0, 0, [], 0)
		self.aSpecies = Species(3, 3, 5, self.someTraits, 0)
		self.anotherSpecies = Species(2, 5, 7, self.someTraits, 0)
		self.yetAnotherSpecies = Species(1, 5, 7, self.someTraits, 0)
		self.yetAnotherYetAnotherSpecies = Species(2, 5, 7, self.someTraits, 0)

		self.carnivore = Species(3, 5, 5, ["carnivore"], 0)
		self.carnivoreAmbush = Species(3, 3, 5, self.someTraits, 0)
		self.carnivoreClimber = Species(3, 3, 5, ["carnivore", "climbing"], 0)
		self.smallCarnivorePackHunter = Species(3, 1, 5, ["carnivore", "pack-hunting"], 0)
		self.warningCall = Species(1, 1, 2, ["warning-call"], 0)
		self.vulnerable = Species(1, 1, 2, [], 0)
		self.burrowSuccess = Species(2, 1, 2, ["burrowing"], 0)
		self.burrowFail = Species(0, 1, 2, ["burrowing"], 0)
		self.climbing = Species(1, 1, 2, ["climbing"], 0)
		self.smallHardShell = Species(1, 1, 2, ["hard-shell"], 0)
		self.bigHardShell = Species(1, 4, 2, ["hard-shell"], 0)
		self.smallHerding = Species(1, 1, 3, ["herding"], 0)
		self.bigHerding = Species(1, 5, 5, ["herding"], 0)
		self.herdingHorns = Species(1, 3, 4, ["herding", "horns"], 0)
		self.smallSymbiosis = Species(1, 1, 2, ["symbiosis"], 0)
		self.bigSymbiosis = Species(1, 5, 5, ["symbiosis"], 0)

	def tearDown(self):
		del self.someTraits 
		del self.defaultSpecies 
		del self.aSpecies 
		del self.anotherSpecies 
		del self.yetAnotherSpecies 
		del self.yetAnotherYetAnotherSpecies 

		del self.carnivore
		del self.carnivoreAmbush
		del self.carnivoreClimber
		del self.smallCarnivorePackHunter
		del self.warningCall
		del self.vulnerable
		del self.burrowSuccess
		del self.burrowFail
		del self.climbing
		del self.smallHardShell
		del self.bigHardShell
		del self.smallHerding
		del self.bigHerding
		del self.herdingHorns

	def testComparators(self):
		self.assertTrue(self.aSpecies.compare(False) > 0)
		self.assertTrue(self.aSpecies.compare(self.anotherSpecies) < 0)
		self.assertTrue(self.anotherSpecies.compare(self.aSpecies) > 0)
		self.assertTrue(self.aSpecies.compare(self.carnivoreAmbush) == 0)
		self.assertTrue(self.yetAnotherSpecies.compare(self.aSpecies) > 0)
		self.assertTrue(self.anotherSpecies.compare(self.yetAnotherYetAnotherSpecies) == 0)

	def testHasTrait(self):
		self.assertTrue(self.aSpecies.hasTrait("carnivore"))
		self.assertTrue(self.aSpecies.hasTrait("ambush"))
		self.assertFalse(self.aSpecies.hasTrait("Ambush"))
		self.assertFalse(self.aSpecies.hasTrait("invincibility"))

	def testIsAttackable(self):
		self.assertTrue(Species.isAttackable(self.vulnerable, self.carnivore, False, False))

		self.assertFalse(Species.isAttackable(self.vulnerable, self.carnivore, self.warningCall, False))
		self.assertFalse(Species.isAttackable(self.vulnerable, self.carnivore, False, self.warningCall))
		self.assertFalse(Species.isAttackable(self.vulnerable, self.carnivore, self.warningCall, self.warningCall))
		self.assertTrue(Species.isAttackable(self.vulnerable, self.carnivoreAmbush, self.warningCall, self.warningCall))

		self.assertFalse(Species.isAttackable(self.burrowSuccess, self.carnivore, False, False))
		self.assertTrue(Species.isAttackable(self.burrowFail, self.carnivore, False, False))

		self.assertFalse(Species.isAttackable(self.climbing, self.carnivore, False, False))
		self.assertTrue(Species.isAttackable(self.climbing, self.carnivoreClimber, False, False))

		self.assertFalse(Species.isAttackable(self.bigHardShell, self.carnivore, False, False))
		self.assertFalse(Species.isAttackable(self.bigHardShell, self.smallCarnivorePackHunter, False, False))
		self.assertTrue(Species.isAttackable(self.smallHardShell, self.smallCarnivorePackHunter, False, False))
		self.assertTrue(Species.isAttackable(self.smallHardShell, self.carnivore, False, False))

		self.assertFalse(Species.isAttackable(self.bigHerding, self.carnivore, False, False))
		self.assertFalse(Species.isAttackable(self.herdingHorns, self.carnivore, False, False))
		self.assertTrue(Species.isAttackable(self.smallHerding, self.carnivore, False, False))

		self.assertFalse(Species.isAttackable(self.smallSymbiosis, self.carnivore, False, self.bigHardShell))
		self.assertTrue(Species.isAttackable(self.bigSymbiosis, self.carnivore, False, self.vulnerable))


if __name__ == "__main__":
	unittest.main()
