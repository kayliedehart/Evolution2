import unittest
from dealer import *
from species import Species
from playerState import PlayerState
from traitCard import TraitCard
from action4 import Action4
from gainPopulation import GainPopulation
from gainBodySize import GainBodySize
from buySpeciesBoard import BuySpeciesBoard
from replaceTrait import ReplaceTrait

class TestDealer(unittest.TestCase):

	def setUp(self):
		self.t1 = TraitCard("horns", 3)
		self.t2 = TraitCard("ambush", 1)
		self.t3 = TraitCard("carnivore", 2)
		self.t4 = TraitCard("fat-tissue", 0)
		self.t5 = TraitCard("foraging", 3)
		self.vegHorns = Species(1, 2, 3, [TraitCard("horns")], 0)
		self.vegCoop = Species(1, 2, 3, [TraitCard("cooperation")], 0)
		self.fat = Species(4, 3, 4, [TraitCard("fat-tissue")], 3)
		self.fatScav = Species(2, 3, 4, [TraitCard("fat-tissue"), TraitCard("scavenger")], 1)
		self.fatFor = Species(4, 3, 4, [TraitCard("fat-tissue"), TraitCard("foraging")], 1)
		self.carnCoop = Species(3, 4, 5, [TraitCard("carnivore"), TraitCard("cooperation")], 0)
		self.carnForage = Species(3, 4, 5, [TraitCard("carnivore"), TraitCard("foraging")], 0)
		self.carnForage1 = Species(3, 4, 5, [TraitCard("carnivore"), TraitCard("foraging")], 0)
		self.extinct = Species(0, 0, 0, [], 0)
		self.p1 = PlayerState(1, 0, [self.vegCoop, self.fat, self.carnForage], [])
		self.p2 = PlayerState(2, 0, [self.vegHorns, self.fatScav, self.carnCoop], [])
		self.p3 = PlayerState(3, 0, [self.vegCoop, self.carnCoop, self.carnForage1], [])
		self.p4 = PlayerState(4, 0, [self.vegCoop], [])
		self.p5 = PlayerState(5, 0, [self.vegHorns], [])
		self.p6 = PlayerState(6, 0, [self.carnCoop], [])
		self.p7 = PlayerState(7, 0, [self.fatScav], [])
		self.p8 = PlayerState(8, 0, [self.fatFor, self.extinct], [])
		self.dealer = Dealer([self.p1, self.p2, self.p3], 3, [self.t1, self.t2, self.t3, self.t4, self.t5])
		self.p2dealer = Dealer([self.p6, self.p5], 3, [])
		self.p3dealer = Dealer([self.p8], 3, [self.t1, self.t2, self.t3, self.t4, self.t5])


		self.xstep3spec = Species(0, 5, 2, [TraitCard("foraging")], 0)
		self.xstep3p = PlayerState(1, 0, [self.xstep3spec], [])
		self.xstep3deal = Dealer([self.xstep3p], 5, [])

		# 8949-0357-4
		self.pCFS1 = PlayerState(1, 3, [Species(4, 2, 5, [TraitCard("carnivore"), TraitCard("cooperation")], 0), 
			Species(1, 3, 4, [TraitCard("foraging"), TraitCard("carnivore"), TraitCard("scavenger")], 0)], [])
		self.pCFS2 = PlayerState(2, 4, [Species(2, 3, 3, [TraitCard("burrowing")], 0)], [])
		self.pCFS3 = PlayerState(3, 5, [], [])
		self.dCFS = Dealer([self.pCFS1, self.pCFS2, self.pCFS3], 10, [])

		# for step4
		self.t6 = TraitCard("herding", 0)
		self.defSpec = Species(0, 0, 1, [], 0)
		self.specWGrownBody = Species(0, 1, 1, [], 0)
		self.specW3t = Species(0, 0, 1, [self.t3, self.t4, self.t5], 0)
		self.specWAll = Species(2, 1, 2, [self.t4], 1)
		self.playerWithManyCards = PlayerState(1, 0, [], [self.t1, self.t2, self.t3, self.t4, self.t5, self.t6])
		self.playerForAll = PlayerState(1, 0, [self.specWAll], [])
		self.playerFor3t = PlayerState(1, 0, [self.specW3t], [self.t6])
		self.playerForDefSpec = PlayerState(1, 0, [self.defSpec], [self.t5, self.t6])
		self.playerForBodyNewSpec = PlayerState(1, 0, [self.specWGrownBody], [self.t3, self.t4, self.t5, self.t6])
		self.noAct = Action4(0, [], [], [], [])
		self.actGP = Action4(0, [GainPopulation(0, 0)], [], [], [])
		self.actGB = Action4(0, [], [GainBodySize(0, 1)], [], [])
		self.actRT = Action4(0, [], [], [], [ReplaceTrait(0, 1, 1)])
		self.actBT0t = Action4(0, [], [], [BuySpeciesBoard(1, [])], [])
		self.actBT1t = Action4(0, [], [], [BuySpeciesBoard(1, [2])], [])
		self.actBT2t = Action4(0, [], [], [BuySpeciesBoard(1, [2, 3])], [])
		self.actBT3t = Action4(0, [], [], [BuySpeciesBoard(1, [2, 3, 4])], [])
		self.actBT4t = Action4(0, [], [], [BuySpeciesBoard(1, [2, 3, 4, 5])], [])
		self.addBodyToNewSpec = Action4(0, [GainPopulation(1, 1)], [], [BuySpeciesBoard(2, [3])], [])
		self.actAll = Action4(0, [GainPopulation(0, 1)], [GainBodySize(0, 2)], [BuySpeciesBoard(4, [5])], [ReplaceTrait(0, 0, 3)])
		self.simpleDealerForStep4 = Dealer([self.playerWithManyCards], 0, [])
		self.dealerForRevokingCards = Dealer([PlayerState(1, 0, [], [self.t1, self.t2]), 
											  PlayerState(2, 0, [], [self.t3, self.t4, self.t5]),
											  PlayerState(3, 0, [], [self.t6])], 0, [])

		self.dealerManyActions = Dealer([PlayerState(1, 0, [self.defSpec], 
												[self.t1, self.t2]), 
										PlayerState(2, 0, [self.vegHorns, self.fatScav, self.carnCoop], 
												[self.t3, self.t4, self.t5, self.t6, self.t1]),
										PlayerState(3, 0, [self.vegCoop, self.carnCoop, self.carnForage1], 
												[self.t6])], 
										0, [])

	def tearDown(self):
		del self.vegHorns 
		del self.vegCoop
		del self.fat
		del self.fatScav 
		del self.carnCoop
		del self.carnForage
		del self.carnForage1
		del self.p1 
		del self.p2
		del self.p3
		del self.p4
		del self.p5
		del self.p6
		del self.p7
		del self.p8
		del self.t1 
		del self.t2
		del self.t3
		del self.t4
		del self.t5
		del self.dealer
		del self.p2dealer
		del self.p3dealer

		del self.xstep3spec
		del self.xstep3p
		del self.xstep3deal

		# 8949-0357-4
		del self.pCFS1
		del self.pCFS2
		del self.pCFS3
		del self.dCFS

		# for step4
		del self.t6
		del self.defSpec
		del self.specWGrownBody
		del self.specW3t
		del self.specWAll
		del self.playerWithManyCards
		del self.playerFor3t
		del self.playerForAll
		del self.playerForDefSpec
		del self.playerForBodyNewSpec
		del self.noAct
		del self.actGP
		del self.actGB
		del self.actRT
		del self.actBT0t
		del self.actBT1t
		del self.actBT2t
		del self.actBT3t
		del self.actBT4t
		del self.addBodyToNewSpec
		del self.actAll	
		del self.simpleDealerForStep4
		del self.dealerForRevokingCards
		del self.dealerManyActions

	# WRONG TESTS
	# 8179-2198-7
	# def testFest11_1(self):
	# 	tf11_1deal = Dealer([PlayerState(1, 0, [Species(0, 3, 2, [TraitCard("long-neck"), TraitCard("foraging"), TraitCard("cooperation")], 0),
	# 											Species(0, 3, 3, [TraitCard("cooperation"), TraitCard("carnivore")], 0),
	# 											Species(0, 2, 1, [], 0),
	# 											Species(0, 2, 2, [TraitCard("fat-tissue"), TraitCard("carnivore")], 2)], [TraitCard("carnivore", 5)]), 
	# 		PlayerState(2, 0, [Species(0, 7, 7, [TraitCard("long-neck"), TraitCard("fertile"), TraitCard("fat-tissue")], 7), 
	# 						   Species(0, 2, 3, [TraitCard("fertile")], 0)], [TraitCard("carnivore", 6)]), 
	# 		PlayerState(3, 0, [Species(0, 5, 2, [TraitCard("herding"), TraitCard("carnivore")], 0)], [TraitCard("carnivore", 7)])], 0, [])
	# 	mtAct = Action4(0, [], [], [], [])
	# 	tf11_1deal.step4([mtAct, mtAct, mtAct])
	# 	self.assertEqual(tf11_1deal.players[1].species[0].population, 4)

	# # 8179-2198-8
	# def testFest11_2(self):
	# 	tf11_2deal = Dealer([PlayerState(1, 0, [Species(0, 3, 2, [TraitCard("long-neck"), TraitCard("foraging"), TraitCard("cooperation")], 0),
	# 											Species(0, 3, 6, [TraitCard("cooperation")], 0),
	# 											Species(0, 2, 2, [], 0),
	# 											Species(0, 2, 2, [TraitCard("fat-tissue")], 2)], [TraitCard("foraging", 3)]), 
	# 		PlayerState(2, 0, [Species(0, 7, 7, [TraitCard("long-neck"), TraitCard("cooperation"), TraitCard("fat-tissue")], 7), 
	# 						   Species(0, 2, 7, [TraitCard("fertile")], 0)], [TraitCard("warning-call", 2)]), 
	# 		PlayerState(3, 0, [Species(0, 5, 2, [TraitCard("herding"), TraitCard("fertile")], 0)], [TraitCard("carnivore", 0)])], 0, [])
	# 	mtAct = Action4(0, [], [], [], [])
	# 	tf11_2deal.step4([mtAct, mtAct, mtAct])
	# 	self.assertEqual(tf11_2deal.players[1].species[0].population, 7)


	def testEndOfTurn(self):
		self.carnForage.food = 0
		self.assertEqual(self.p1.foodbag, 0)
		self.assertEqual(self.p2.foodbag, 0)
		self.assertEqual(self.p3.foodbag, 0)
		self.assertEqual(self.fat.food, 4)
		self.assertEqual(self.vegHorns.food, 1)
		self.assertEqual(self.fat.population, 4)
		self.assertEqual(self.vegHorns.population, 3)
		self.assertEqual(len(self.dealer.deck), 5)
		self.assertEqual(len(self.p1.species), 3)
		self.assertEqual(len(self.p2.species), 3)
		self.assertEqual(len(self.p3.species), 3)
		self.dealer.endOfTurn()
		self.assertEqual(self.p1.foodbag, 5)
		self.assertEqual(self.p2.foodbag, 6)
		# self.assertEqual(self.p3.foodbag, 7) p3 shares a species w/p1 and thus this breaks
		self.assertEqual(self.fat.food, 0)
		self.assertEqual(self.vegHorns.food, 0)
		self.assertEqual(self.fat.population, 4)
		self.assertEqual(self.vegHorns.population, 1)
		self.assertEqual(len(self.dealer.deck), 0)
		self.assertEqual(len(self.p1.species), 2)
		self.assertEqual(len(self.p2.species), 3)
		self.assertEqual(len(self.p3.species), 1)
		self.assertEqual(self.p1.hand, [self.t1, self.t2])
		self.assertEqual(self.p3.hand, [self.t3, self.t4, self.t5])

	def testRunGame(self):
		gameDealer = Dealer([self.p1, self.p2, self.p3], 0)
		[self.assertEqual(player.foodbag, 0) for player in gameDealer.players]
		try: 
			gameDealer.runGame()
		except SystemExit: # because gameOver() quits
			self.assertTrue(len(gameDealer.deck) < 12)

		del gameDealer

	def testNumCardsThisTurn(self):
		self.assertEqual(len(self.dealer.players), 3)
		self.assertEqual(len(self.p1.species), 3)
		self.assertEqual(len(self.p2.species), 3)
		self.assertEqual(len(self.p3.species), 3)
		self.assertEqual(self.dealer.numCardsThisTurn(), 18)

	def testSteps2and3(self):
		gameDealer = Dealer([self.p1, self.p2, self.p3], 0)
		[player.start(False) for player in gameDealer.players]
		gameDealer.step1()
		[self.assertEqual(player.foodbag, 0) for player in gameDealer.players]
		gameDealer.steps2and3()
		del gameDealer

	def testFilterCheatActions(self):
		noCheaters = [self.p1, self.p2]
		allGoodActions = [self.addBodyToNewSpec, self.actAll]
		goodDeal = Dealer(noCheaters, 0)
		noCheats = goodDeal.filterCheatActions(allGoodActions)
		self.assertEqual(goodDeal.players, noCheaters)
		self.assertEqual(noCheats, allGoodActions)

		someCheaters = [self.p1, self.p3, self.p2, self.p4]
		someBadActions = [self.addBodyToNewSpec, False, self.actAll, False]
		cheatDeal = Dealer(someCheaters, 0)
		cheatsGone = cheatDeal.filterCheatActions(someBadActions)
		self.assertEqual(cheatsGone, allGoodActions)
		self.assertEqual(cheatDeal.players, noCheaters)

		del someCheaters
		del someBadActions
		del cheatDeal
		del noCheaters
		del allGoodActions
		del goodDeal


	def testStep1(self):
		dealEarlyOn = Dealer([PlayerState(1, 0, [], []), PlayerState(2, 0, [], []), PlayerState(2, 0, [], [])], 0)
		dealEarlyOn.step1()
		for player in dealEarlyOn.players:
			self.assertEqual(len(player.species), 1)
			self.assertEqual(len(player.hand), 4)
		del dealEarlyOn

		dealLaterOn = Dealer([PlayerState(1, 0, [self.vegHorns, self.vegCoop], []), PlayerState(2, 0, [self.carnForage], []), PlayerState(2, 0, [], [])], 0)
		dealLaterOn.step1()
		self.assertEqual(len(dealLaterOn.players[0].species), 2)
		self.assertEqual(len(dealLaterOn.players[0].hand), 5)	
		self.assertEqual(len(dealLaterOn.players[1].species), 1)
		self.assertEqual(len(dealLaterOn.players[1].hand), 4)	
		self.assertEqual(len(dealLaterOn.players[2].species), 1)
		self.assertEqual(len(dealLaterOn.players[2].hand), 4)	
		del dealLaterOn	

	def testStep4(self):
		# successfully adding three traits to a new species
		self.playerWithManyCards = PlayerState(1, 0, [], [self.t1, self.t2, self.t3, self.t4, self.t5, self.t6])
		self.simpleDealerForStep4 = Dealer([self.playerWithManyCards], 0, [])
		self.simpleDealerForStep4.step4([self.actBT3t])
		self.assertEqual(len(self.playerFor3t.hand), 1)
		self.assertEqual(len(self.playerFor3t.species), 1)
		self.assertEqual(len(self.playerFor3t.species[0].traits), 3)
		self.assertEqual(self.simpleDealerForStep4.players[0], self.playerFor3t)
		for card in [self.t1, self.t2, self.t3, self.t4, self.t5]:
			self.assertTrue(card in self.simpleDealerForStep4.discard)
			
		# test adding a species, then growing its population and body and giving it a new trait
		self.playerWithManyCards = PlayerState(1, 0, [], [self.t1, self.t2, self.t3, self.t4, self.t5, self.t6])
		self.simpleDealerForStep4 = Dealer([self.playerWithManyCards], 0, [])
		self.simpleDealerForStep4.step4([self.actAll])
		self.assertEqual(len(self.playerForAll.hand), 0)
		self.assertEqual(len(self.playerForAll.species), 1)
		self.assertEqual(len(self.playerForAll.species[0].traits), 1)
		self.assertEqual(self.simpleDealerForStep4.players[0], self.playerForAll)
		self.assertEqual(self.simpleDealerForStep4.players[0].species, [self.specWAll])
		for card in [self.t1, self.t2, self.t3, self.t4, self.t5, self.t6]:
			self.assertTrue(card in self.simpleDealerForStep4.discard)
		self.assertEqual(self.simpleDealerForStep4.wateringHole, 0)

	def testRevokePlayedCards(self):
		# revoke cards from the hands of players
		# if there is an error with indexing, then Player w/id 2 will fail spectacularly
		self.dealerForRevokingCards.cardsPlayed = [(0, 1), (1, 1), (1, 0), (2, 0)]
		self.dealerForRevokingCards.revokePlayedCards()
		self.assertEqual(len(self.dealerForRevokingCards.cardsPlayed), 0)
		self.assertEqual(self.dealerForRevokingCards.players[0].hand, [self.t1])
		self.assertEqual(self.dealerForRevokingCards.players[1].hand, [self.t5])
		self.assertEqual(len(self.dealerForRevokingCards.players[2].hand), 0)

	def testPlayerGains(self):

		self.assertEqual(self.dealerManyActions.players[0].species[0].body, 0)
		self.assertEqual(self.dealerManyActions.players[0].species[0].population, 1)
		self.assertEqual(len(self.dealerManyActions.discard), 0)
		
		self.dealerManyActions.playerGains(0, self.actGB.GB, self.dealerManyActions.players[0].addBody)

		self.assertEqual(self.dealerManyActions.players[0].species[0].body, 1)
		self.assertEqual(self.dealerManyActions.players[0].species[0].population, 1)
		self.assertEqual(len(self.dealerManyActions.discard), 1)

		self.dealerManyActions.playerGains(0, self.actGP.GP, self.dealerManyActions.players[0].addPopulation)

		self.assertEqual(self.dealerManyActions.players[0].species[0].body, 1)
		self.assertEqual(self.dealerManyActions.players[0].species[0].population, 2)
		self.assertEqual(len(self.dealerManyActions.discard), 2)

	def testCreateSpecBoard(self):
		# self.actBT3t = Action4(0, [], [], [BuySpeciesBoard(1, [2, 3, 4])], [])
		self.assertEqual(len(self.dealerManyActions.discard), 0)
		self.assertEqual(len(self.dealerManyActions.players[1].species), 3)

		self.dealerManyActions.createSpecBoard(1, self.actBT3t.BT)

		self.assertEqual(len(self.dealerManyActions.discard), 4)
		self.assertEqual(len(self.dealerManyActions.players[1].species), 4)
		self.assertTrue(self.dealerManyActions.players[1].species[3].hasTrait("herding"))
		self.assertTrue(self.dealerManyActions.players[1].species[3].hasTrait("foraging"))
		self.assertTrue(self.dealerManyActions.players[1].species[3].hasTrait("horns"))
		self.assertFalse(self.dealerManyActions.players[1].species[3].hasTrait("fat-tissue"))	


	def testBuyUpgrades(self):
		self.assertEqual(len(self.dealerManyActions.discard), 0)
		self.assertEqual(len(self.dealerManyActions.players[1].species), 3)
		self.dealerManyActions.buyUpgrades(1, self.actBT3t)

		self.assertEqual(len(self.dealerManyActions.discard), 4)
		self.assertEqual(len(self.dealerManyActions.players[1].species), 4)
		self.assertTrue(self.dealerManyActions.players[1].species[3].hasTrait("herding"))
		self.assertTrue(self.dealerManyActions.players[1].species[3].hasTrait("foraging"))
		self.assertTrue(self.dealerManyActions.players[1].species[3].hasTrait("horns"))
		self.assertFalse(self.dealerManyActions.players[1].species[3].hasTrait("fat-tissue"))

	def testGetPlayerCards(self):
		# self.dealerForRevokingCards = Dealer([PlayerState(1, 0, [], [self.t1, self.t2]), 
		# 							  PlayerState(2, 0, [], [self.t3, self.t4, self.t5]),
		# 							  PlayerState(3, 0, [], [self.t6])], 0, [])
		self.assertEqual(self.dealerForRevokingCards.getPlayerCards([(0, 1), (1, 1), (1, 0), (2, 0)]), 
							[self.t2, self.t4, self.t3, self.t6])

	def testUpdateDiscards(self):		
		# self.dealerForRevokingCards = Dealer([PlayerState(1, 0, [], [self.t1, self.t2]), 
		# 							  PlayerState(2, 0, [], [self.t3, self.t4, self.t5]),
		# 							  PlayerState(3, 0, [], [self.t6])], 0, [])
		self.dealerForRevokingCards.discard = [self.t1]
		self.dealerForRevokingCards.cardsPlayed = [(0, 1)]
		self.dealerForRevokingCards.updateDiscards([(1, 1), (1, 0)])
		self.assertEqual(self.dealerForRevokingCards.discard, [self.t1, self.t4, self.t3])
		self.assertEqual(self.dealerForRevokingCards.cardsPlayed, [(0, 1), (1, 1), (1, 0)])

	def testReplenishWateringHole(self):
		self.assertEqual(len(self.dealerManyActions.discard), 0)
		self.assertEqual(self.dealerManyActions.wateringHole, 0)
		
		self.dealerManyActions.replenishWateringHole([(0,0), (1,0), (2, 0)])

		self.assertEqual(len(self.dealerManyActions.discard), 3)
		self.assertEqual(self.dealerManyActions.wateringHole, 5)
		

	def testPrelimAutoFeedings(self):
		self.dealerForAutoFeeds = Dealer([PlayerState(1, 0, [Species(0, 2, 3, [TraitCard("fertile"), TraitCard("fat-tissue")], 2)], []),
									PlayerState(1, 0, [Species(0, 2, 3, [TraitCard("fat-tissue")], 0)], []),
									PlayerState(3, 0, [Species(0, 2, 3, [TraitCard("fertile"), TraitCard("long-neck")], 0)], [])], 
									10, [])
		self.assertEqual(len(self.dealerForAutoFeeds.discard), 0)
		self.assertEqual(self.dealerForAutoFeeds.wateringHole, 10)
		self.assertEqual(self.dealerForAutoFeeds.players[0].species[0].population, 3)
		self.assertEqual(self.dealerForAutoFeeds.players[0].species[0].fatFood, 2)
		self.assertEqual(self.dealerForAutoFeeds.players[0].species[0].food, 0)
		self.assertEqual(self.dealerForAutoFeeds.players[0].species[0].body, 2)

		self.assertEqual(self.dealerForAutoFeeds.players[1].species[0].population, 3)
		self.assertEqual(self.dealerForAutoFeeds.players[1].species[0].fatFood, 0)
		self.assertEqual(self.dealerForAutoFeeds.players[1].species[0].food, 0)
		self.assertEqual(self.dealerForAutoFeeds.players[1].species[0].body, 2)

		self.assertEqual(self.dealerForAutoFeeds.players[2].species[0].population, 3)
		self.assertEqual(self.dealerForAutoFeeds.players[2].species[0].fatFood, 0)
		self.assertEqual(self.dealerForAutoFeeds.players[2].species[0].food, 0)
		self.assertEqual(self.dealerForAutoFeeds.players[2].species[0].body, 2)

		self.dealerForAutoFeeds.prelimAutoFeedings()

		self.assertEqual(len(self.dealerForAutoFeeds.discard), 0)
		self.assertEqual(self.dealerForAutoFeeds.wateringHole, 9)
		self.assertEqual(self.dealerForAutoFeeds.players[0].species[0].population, 4)
		self.assertEqual(self.dealerForAutoFeeds.players[0].species[0].fatFood, 0)
		self.assertEqual(self.dealerForAutoFeeds.players[0].species[0].food, 2)
		self.assertEqual(self.dealerForAutoFeeds.players[0].species[0].body, 2)

		self.assertEqual(self.dealerForAutoFeeds.players[1].species[0].population, 3)
		self.assertEqual(self.dealerForAutoFeeds.players[1].species[0].fatFood, 0)
		self.assertEqual(self.dealerForAutoFeeds.players[1].species[0].food, 0)
		self.assertEqual(self.dealerForAutoFeeds.players[1].species[0].body, 2)

		self.assertEqual(self.dealerForAutoFeeds.players[2].species[0].population, 4)
		self.assertEqual(self.dealerForAutoFeeds.players[2].species[0].fatFood, 0)
		self.assertEqual(self.dealerForAutoFeeds.players[2].species[0].food, 1)
		self.assertEqual(self.dealerForAutoFeeds.players[2].species[0].body, 2)


		

	def testReplaceTraits(self):
		playerForReplacingTraits = PlayerState(1, 0, [Species(0, 0, 1, [TraitCard("foraging"), TraitCard("herding")], 0)], 
												[TraitCard("carnivore"), TraitCard("horns")])
		dealerForReplacingTraits = Dealer([playerForReplacingTraits], 0, [])
		dealerForReplacingTraits.replaceTraits(0, self.actRT)
		# the card is still in hand -- it will be removed in the step4 method, not here
		self.assertEqual(dealerForReplacingTraits.players[0].hand, [TraitCard("carnivore"), TraitCard("horns")]) 
		self.assertEqual(dealerForReplacingTraits.players[0].species[0].traits, [TraitCard("foraging"), TraitCard("horns")])

	def testXstep(self):
		self.assertEqual(self.xstep3spec.food, 0)
		self.xstep3deal.feed1()
		self.assertEqual(self.xstep3spec.food, 2)
		self.assertEqual(self.xstep3deal.wateringHole, 3)

	def testToDict(self):		
		self.p2dealer.deck = []
		self.assertEqual(self.p2dealer.toDict(), {"wateringHole": 3, "deck": [], 
			"players": [{"num": 6, "species": 
							[{"food": 3, "body": 4, "population": 5, "traits": [{"name":"carnivore", "food": 0}, {"name":"cooperation", "food":0}], "fatFood": 0}], 
							"hand": [], "foodbag": 0}, 
						{"num": 5, "species": 
							[{"food": 1, "body": 2, "population": 3, "traits": [{"name":"horns", "food": 0}], "fatFood": 0}], 
							"hand": [], "foodbag": 0}]})

	def testRemovePlayer(self):
		self.assertEqual(len(self.dealer.players), 3)
		self.assertTrue(self.p1 in self.dealer.currentlyFeeding)
		self.assertTrue(self.p2 in self.dealer.currentlyFeeding)
		self.assertTrue(self.p3 in self.dealer.currentlyFeeding)
		self.dealer.removePlayerFromTurn(self.p2)
		self.assertEqual(len(self.dealer.players), 3)
		self.assertTrue(self.p1 in self.dealer.currentlyFeeding)
		self.assertFalse(self.p2 in self.dealer.currentlyFeeding)
		self.assertTrue(self.p3 in self.dealer.currentlyFeeding)
		# check exception raise condition

	def testFeedFromWateringHole(self):
		self.assertEqual(self.dealer.wateringHole, 3)
		self.dealer.feedFromWateringHole(self.p1, 2)
		self.assertEqual(self.dealer.wateringHole, 1)
		self.assertEqual(self.carnForage.food, 5)

		self.assertEqual(self.dealer.wateringHole, 1)
		self.assertEqual(self.vegCoop.food, 1)
		self.assertEqual(self.carnCoop.food, 3)
		self.dealer.feedFromWateringHole(self.p3, 0)
		self.assertEqual(self.dealer.wateringHole, 0)
		self.assertEqual(self.vegCoop.food, 2)
		self.assertEqual(self.carnCoop.food, 3)

		self.dealer.wateringHole = 3
		self.assertEqual(self.carnForage1.food, 3)
		self.dealer.feedFromWateringHole(self.p3, 0)
		self.assertEqual(self.vegCoop.food, 3)
		self.assertEqual(self.carnCoop.food, 4)
		self.assertEqual(self.carnForage1.food, 4)
		self.assertEqual(self.dealer.wateringHole, 0)

	def testExecuteAttack(self):
		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.vegCoop.population, 3)
		self.assertEqual(self.carnCoop.food, 3)

		self.dealer.executeAttack(self.p3, self.p1, 1, 0)
		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.vegCoop.population, 2)
		self.assertEqual(self.carnCoop.food, 4)
		self.assertEqual(self.dealer.wateringHole, 0)

		self.dealer.executeAttack(self.p3, self.p2, 1, 0)
		self.assertEqual(self.carnCoop.population, 4)
		self.assertEqual(self.vegHorns.population, 2)

	def testExtinctSpecies(self):
		# nothing changes if non-extinct
		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(len(self.p3.hand), 0)
		self.assertEqual(len(self.dealer.deck), 5)
		self.dealer.extinctSpecies(self.p3, 1)
		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(len(self.p3.hand), 0)
		self.assertEqual(len(self.dealer.deck), 5)

		self.assertEqual(self.extinct.population, 0)
		self.assertEqual(len(self.p8.hand), 0)
		self.assertEqual(len(self.p3dealer.deck), 5)
		self.p3dealer.extinctSpecies(self.p8, 1)
		self.assertEqual(len(self.p8.hand), 2)
		self.assertEqual(self.p8.hand, [self.t1, self.t2])
		self.assertEqual(len(self.p3dealer.deck), 3)
		self.assertEqual(self.p3dealer.deck, [self.t3, self.t4, self.t5])

	# TODO: update to match new matthias test spec
	# def testDistributeCards(self):
	# 	self.assertEqual(len(self.p3.hand), 0)
	# 	self.assertEqual(len(self.dealer.deck), 5)
	# 	self.dealer.distributeCards(self.p3, 2)
	# 	self.assertEqual(self.p3.hand, [self.t1, self.t2])
	# 	self.assertEqual(self.dealer.deck, [self.t3, self.t4, self.t5])

	# 	self.assertEqual(len(self.p3.hand), 2)
	# 	self.assertEqual(len(self.dealer.deck), 3)
	# 	self.dealer.distributeCards(self.p3, 2)
	# 	self.assertEqual(self.p3.hand, [self.t1, self.t2, self.t3, self.t4])
	# 	self.assertEqual(self.dealer.deck, [self.t5])

	# 	self.assertEqual(len(self.p3.hand), 4)
	# 	self.assertEqual(len(self.dealer.deck), 1)
	# 	self.dealer.distributeCards(self.p3, 2)
	# 	self.assertEqual(self.p3.hand, [self.t1, self.t2, self.t3, self.t4, self.t5])
	# 	self.assertEqual(self.dealer.deck, [])

	def testAutoFeed(self):
		self.assertFalse(self.dealer.autoFeed(self.p1))
		self.assertFalse(self.dealer.autoFeed(self.p2))
		self.assertEqual(self.vegCoop.food, 1)
		self.assertTrue(self.dealer.autoFeed(self.p4))
		self.assertEqual(self.vegCoop.food, 2)
		
	def testQueryFeed(self):
		self.assertEqual(self.vegCoop.food, 1)
		self.assertFalse(self.dealer.queryFeed(self.p4))
		self.assertEqual(self.vegCoop.food, 2)

		self.assertEqual(self.fatScav.fatFood, 1)
		self.assertFalse(self.dealer.queryFeed(self.p7))
		self.assertEqual(self.fatScav.fatFood, 3)
		self.assertEqual(self.dealer.wateringHole, 0)

		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.carnCoop.food, 3)
		self.assertEqual(self.vegHorns.population, 3)
		self.assertTrue(self.p2dealer.queryFeed(self.p6))
		self.assertEqual(self.carnCoop.population, 4)
		self.assertEqual(self.carnCoop.food, 4)
		self.assertEqual(self.vegHorns.population, 2)

	def testScavengeFeed(self):
		self.assertEqual(self.fatScav.food, 2)
		self.assertEqual(self.dealer.wateringHole, 3)
		self.dealer.scavengeFeed(self.p1)
		self.assertEqual(self.fatScav.food, 3)
		self.assertEqual(self.dealer.wateringHole, 2)

		self.dealer.scavengeFeed(self.p1)
		self.dealer.scavengeFeed(self.p1)
		self.dealer.scavengeFeed(self.p1)
		self.assertEqual(self.fatScav.food, 4)
		self.assertEqual(self.dealer.wateringHole, 1)

		self.carnCoop.traits.append(TraitCard("scavenger"))
		self.vegCoop.traits.append(TraitCard("scavenger"))
		self.assertEqual(self.vegCoop.food, 1)
		self.assertEqual(self.carnCoop.food, 3)
		self.dealer.scavengeFeed(self.p1)
		self.assertEqual(self.vegCoop.food, 2)
		self.assertEqual(self.carnCoop.food, 3)
		self.assertEqual(self.dealer.wateringHole, 0)


	def testFeed1(self):
		self.assertEqual(self.vegCoop.food, 1)
		self.dealer.feed1()
		self.assertEqual(self.vegCoop.food, 2)
		self.assertEqual(self.dealer.wateringHole, 2)

		self.assertEqual(self.carnCoop.population, 5)
		self.assertEqual(self.carnCoop.food, 3)
		self.assertEqual(self.vegHorns.population, 3)
		self.p2dealer.feed1()
		self.assertEqual(self.carnCoop.population, 4)
		self.assertEqual(self.carnCoop.food, 4)
		self.assertEqual(self.vegHorns.population, 2)

		self.assertEqual(self.fatFor.fatFood, 1)
		self.assertEqual(self.fatFor.food, 4)
		self.p3dealer.feed1()
		self.assertEqual(self.fatFor.fatFood, 3)
		self.assertEqual(self.fatFor.food, 4)
		self.assertEqual(self.p3dealer.wateringHole, 1)

		# a user without any species should not be deleted from players
		# but should be deleted from currentlyFeeding 
		# 0067-2657-1
		pNoSpecies1 = PlayerState(1, 0, [], [])
		pNoSpecies2 = PlayerState(2, 0, [], [])
		pNoSpecies3 = PlayerState(3, 0, [], [])
		dNoSpecies = Dealer([pNoSpecies1, pNoSpecies2, pNoSpecies3], 5, [])
		self.assertEqual(len(dNoSpecies.players), 3)
		self.assertEqual(len(dNoSpecies.currentlyFeeding), 3)
		dNoSpecies.feed1()
		self.assertEqual(len(dNoSpecies.players), 3)
		self.assertEqual(len(dNoSpecies.currentlyFeeding), 2)
		self.assertFalse(pNoSpecies1 in dNoSpecies.currentlyFeeding)

		# a user who can no longer attack/feed should not be deleted from players
		# but should be deleted from currentlyFeeding 
		# 0067-2657-7
		pNoAtkSpecies1 = PlayerState(1, 0, [Species(0, 1, 1, [TraitCard("carnivore")], 0), 
					Species(1, 1, 1, [TraitCard("horns"), TraitCard("cooperation")], 0), 
					Species(1, 1, 1, [], 0)], [])
		pNoAtkSpecies2 = PlayerState(2, 0, [Species(0, 1, 1, [TraitCard("hard-shell")], 0)], [])
		pNoAtkSpecies3 = PlayerState(3, 0, [Species(0, 1, 1, [TraitCard("cooperation"), TraitCard("scavenger"), TraitCard("climbing")], 0), 
					Species(0, 1, 2, [TraitCard("cooperation"), TraitCard("scavenger"), TraitCard("climbing")], 0), 
					Species(0, 1, 4, [TraitCard("foraging"), TraitCard("hard-shell")], 0)], [])
		dNoAtkSpecies = Dealer([pNoAtkSpecies1, pNoAtkSpecies2, pNoAtkSpecies3], 5, [])
		self.assertEqual(len(dNoAtkSpecies.players), 3)
		self.assertEqual(len(dNoAtkSpecies.currentlyFeeding), 3)
		dNoAtkSpecies.feed1()
		self.assertEqual(len(dNoAtkSpecies.players), 3)
		self.assertEqual(len(dNoAtkSpecies.currentlyFeeding), 2)
		self.assertFalse(pNoAtkSpecies1 in dNoAtkSpecies.currentlyFeeding)

		# successfully extincting someone else's species should give two cards to loser
		# 2598-3830-8
		pExtinction1 = PlayerState(3, 2, [Species(3, 4, 4, [TraitCard("carnivore")], 0)], [TraitCard("burrowing", -3)])
		pExtinction2 = PlayerState(2, 42, [Species(0, 3, 4, [TraitCard("climbing")], 0),
					Species(4, 2, 4, [TraitCard("climbing")], 0),
					Species(4, 1, 4, [TraitCard("climbing")], 0)], [TraitCard("climbing", 3)])
		pExtinction3 = PlayerState(4, 100, [Species(0, 7, 1, [], 0)], [])
		dExtinction = Dealer([pExtinction1, pExtinction2, pExtinction3], 9, [TraitCard("burrowing", 3), TraitCard("horns", 3), TraitCard("climbing", 1)])

		self.assertEqual(len(dExtinction.deck), 3)
		dExtinction.feed1()
		self.assertEqual(len(dExtinction.deck), 1)
		self.assertEqual(pExtinction3.hand, [TraitCard("burrowing", 3), TraitCard("horns", 3)])
		self.assertEqual(len(pExtinction3.species), 0)
		self.assertEqual(pExtinction1.species[0].food, 4)
		self.assertEqual(dExtinction.wateringHole, 8)

	def testCoopForgScavenge(self):
		# cooperation + foraging + scavenging
		# 8949-0357-4
		self.dCFS.feed1()
		self.assertEqual(self.pCFS1.species[0].food, 5)
		self.assertEqual(self.pCFS1.species[1].food, 4)
		self.assertEqual(self.pCFS2.species[0].population, 2)
		self.assertEqual(self.pCFS2.species[0].food, 2)
		self.assertEqual(self.pCFS3.species, [])
		self.assertEqual(self.dCFS.wateringHole, 6)


if __name__ == "__main__":
	unittest.main()
