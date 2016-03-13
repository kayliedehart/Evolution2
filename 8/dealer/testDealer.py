import unittest
from species import Species
from playerState import PlayerState
from dealer import *

class TestDealer(unittest.TestCase):

    def setUp(self):
        self.vegHorns = Species(1, 2, 3, ["horns"], 0)
        self.vegCoop = Species(1, 2, 3, ["cooperation"], 0)
        self.fat = Species(2, 3, 4, ["fat-tissue"], 1)
        self.fatScav = Species(2, 3, 4, ["fat-tissue", "scavenging"], 1)
        self.carn = Species(3, 4, 5, ["carnivore"], 0)
        self.carnForage = Species(3, 4, 5, ["carnivore", "foraging"], 0)
        self.p1 = PlayerState(1, 0, [self.vegCoop, self.fat, self.carnForage], [])
        self.p2 = PlayerState(2, 0, [self.vegHorns, self.fatScav, self.carn], [])
        self.p3 = PlayerState(3, 0, [self.vegCoop, self.vegCoop, self.carn], [])
        self.dealer = Dealer([self.p1, self.p2, self.p3], 2, [])

    def tearDown(self):
        del self.vegHorns 
        del self.vegCoop
        del self.fat
        del self.fatScav 
        del self.carn 
        del self.carnForage
        del self.p1 
        del self.p2
        del self.p3
        del self.dealer

    def testFeedFromWateringHole(self):
        pass

    def testExecuteAttack(self):
        pass

    def testAutoFeed(self):
        pass

    def testQueryFeed(self):
        pass

    def testScavengeFeed(self):
        pass

    def testFeed1(self):
        pass