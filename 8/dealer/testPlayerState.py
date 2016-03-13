import unittest
from playerState import *
from traitCard import TraitCard

class TestPlayerState(unittest.TestCase):

	def setUp(self):
		self.p1 = PlayerState(1, 1, [], [])
		self.p2 = PlayerState(2, 1, [], [])
		self.otherp1 = PlayerState(1, 1, [], [])

	def tearDown(self):
		del self.p1
		del self.p2
		del self.otherp1

	def testEqAndMutability(self):
		self.assertNotEqual(self.p1, self.p2)
		self.assertEqual(self.p1, self.otherp1)
		self.p1.hand.append(TraitCard("carnivore", 1))
		self.assertNotEqual(self.p1.hand, self.p2.hand)
		self.assertNotEqual(self.p1, self.otherp1)


if __name__ == "__main__":
	unittest.main()
