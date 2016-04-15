import unittest
from traitCard import TraitCard

class TestTraitCard(unittest.TestCase):
	def setUp(self):
		self.t1 = TraitCard("horns", 3)
		self.t2 = TraitCard("ambush", 1)
		self.t3 = TraitCard("carnivore", 2)
		self.t4 = TraitCard("fat-tissue", 0)
		self.t5 = TraitCard("foraging", 3)

	def tearDown(self):
		del self.t1 
		del self.t2
		del self.t3
		del self.t4
		del self.t5

	def testToDict(self):
		self.assertEqual(self.t1.toDict(), {"name": "horns", "food": 3})

	def testCheckTrait(self):
		goodTrait = "fat-tissue"
		carn = "carnivore"
		warn = "warning-call"
		badTrait = "invincibility"

		self.assertTrue(TraitCard.checkTrait(goodTrait))
		self.assertTrue(TraitCard.checkTrait(carn))
		self.assertTrue(TraitCard.checkTrait(warn))
		
		self.assertFalse(TraitCard.checkTrait(badTrait))

if __name__ == "__main__":
	unittest.main()
