import unittest
from species import *

class TestSpecies(unittest.TestCase):

	def setUp(self):        
		self.someTraits = ["carnivore", "ambush"]
		self.defaultSpecies = Species(0, 0, 0, [], 0)
		self.aSpecies = Species(3, 3, 5, self.someTraits, 0)
		self.anotherSpecies = Species(2, 5, 7, self.someTraits, 0)
		self.yetAnotherSpecies = Species(1, 5, 7, self.someTraits, 0)
		self.yetAnotherYetAnotherSpecies = Species(2, 5, 7, self.someTraits, 0)
		self.fatNoFood = Species(0, 2, 2, ["fat-tissue"], 2)
		self.foodNoFat = Species(2, 2, 2, ["fat-tissue"], 0)
		self.fedUp = Species(2, 2, 2, ["fat-tissue"], 2)

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
		del self.fatNoFood
		del self.foodNoFat
		del self.fedUp

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

	def testToDict(self):
		self.assertEqual(self.aSpecies.toDict(), {"food": 3, "body": 3, "population": 5, "traits": ["carnivore", "ambush"], "fatFood": 0})
		self.assertEqual(self.fatNoFood.toDict(), {"food": 0, "body": 2, "population": 2, "traits": ["fat-tissue"], "fatFood": 2})
		self.assertEqual(self.foodNoFat.toDict(), {"food": 2, "body": 2, "population": 2, "traits": ["fat-tissue"], "fatFood": 0})

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

	def testIsExtinct(self):
		self.assertTrue(self.defaultSpecies.isExtinct())
		self.assertFalse(self.aSpecies.isExtinct())

	def testExecuteAttack(self):
		self.assertEqual(self.aSpecies.food, 3)
		self.assertEqual(self.aSpecies.population, 5)
		self.aSpecies.executeAttack()
		self.assertEqual(self.aSpecies.food, 3)
		self.assertEqual(self.aSpecies.population, 4)
		self.aSpecies.executeAttack()
		self.assertEqual(self.aSpecies.food, 3)
		self.assertEqual(self.aSpecies.population, 3)
		self.aSpecies.executeAttack()
		self.assertEqual(self.aSpecies.food, 2)
		self.assertEqual(self.aSpecies.population, 2)

	def testEatFood(self):
		self.assertEqual(self.aSpecies.food, 3)
		self.aSpecies.eatFood(1)
		self.assertEqual(self.aSpecies.food, 4)

	def testEatFatFood(self):
		self.assertEqual(self.foodNoFat.fatFood, 0)
		self.foodNoFat.eatFatFood(1)
		self.assertEqual(self.foodNoFat.fatFood, 1)

	def testIsHungry(self):
		self.assertTrue(self.aSpecies.isHungry())
		self.assertTrue(self.fatNoFood.isHungry())
		self.assertTrue(self.foodNoFat.isHungry())
		self.assertFalse(self.fedUp.isHungry())

	def testWarningCall(self):
		self.assertTrue(self.vulnerable.checkWarningCall(self.carnivore, False, False))
		self.assertFalse(self.vulnerable.checkWarningCall(self.carnivore, self.warningCall, False))
		self.assertFalse(self.vulnerable.checkWarningCall(self.carnivore, False, self.warningCall))
		self.assertFalse(self.vulnerable.checkWarningCall(self.carnivore, self.warningCall, self.warningCall))

	def testBurrowing(self):
		self.assertEqual(self.burrowSuccess.food, self.burrowSuccess.population)
		self.assertFalse(self.burrowSuccess.checkBurrowing())

		self.assertNotEqual(self.burrowFail.food, self.burrowFail.population)
		self.assertTrue(self.burrowFail.checkBurrowing())

	def testClimbing(self):
		self.assertTrue(self.vulnerable.checkClimbing(self.carnivoreClimber))
		self.assertTrue(self.climbing.checkClimbing(self.carnivoreClimber))
		self.assertFalse(self.climbing.checkClimbing(self.carnivore))

	def testHardShell(self):
		self.assertTrue(self.smallHardShell.checkHardShell(self.carnivore))
		self.assertTrue(self.smallHardShell.checkHardShell(self.smallCarnivorePackHunter))
		self.assertFalse(self.bigHardShell.checkHardShell(self.carnivore))
		self.assertFalse(self.bigHardShell.checkHardShell(self.smallCarnivorePackHunter))

	def testHerding(self):
		self.assertTrue(self.smallHerding.checkHerding(self.carnivore))
		self.assertFalse(self.bigHerding.checkHerding(self.carnivore))
		self.assertFalse(self.herdingHorns.checkHerding(self.carnivore))

	def testSymbiosis(self):
		self.assertFalse(self.smallSymbiosis.checkSymbiosis(self.bigHardShell))
		self.assertTrue(self.bigSymbiosis.checkSymbiosis(self.vulnerable))

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
