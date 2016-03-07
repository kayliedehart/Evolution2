import unittest
from playerState import *
from traitCard import TraitCard

class TestPlayerState(unittest.TestCase):

    def testMutability(self):
        p1 = PlayerState(1, 1, [], [])
        p2 = PlayerState(2, 1, [], [])
        p1.hand.append(TraitCard("carnivore"))

        self.assertNotEqual(p1.hand, p2.hand)


if __name__ == "__main__":
    unittest.main()
