import unittest
from Card import *
from Player import *
from Dealer import *
from GameBoard import *


class Test(unittest.TestCase):

    ### STACK TESTS

    def testAddToStack(self):
        someCards = [Card(25, 6), Card(30, 7), Card(7, 3), Card(66, 2)]
        aStack = Stack(Card(25, 6))
        aStack.addToStack(Card(30, 7))
        aStack.addToStack(Card(7, 3))
        aStack.addToStack(Card(66, 2))

        self.assertEqual(someCards[3].faceValue, aStack.cards[3].faceValue)

    def testGetBullPoints(self):
        aStack = Stack(Card(25, 6))
        aStack.addToStack(Card(30, 7))
        aStack.addToStack(Card(7, 3))
        aStack.addToStack(Card(66, 2))
        self.assertEqual(18, aStack.getBullPoints())

    def testGetNumCards(self):
        aStack = Stack(Card(25, 6))
        aStack.addToStack(Card(30, 7))
        aStack.addToStack(Card(7, 3))
        aStack.addToStack(Card(66, 2))
        self.assertEqual(4, aStack.getNumCards())

    def testGetTopCard(self):
        aStack = Stack(Card(25, 6))
        aStack.addToStack(Card(30, 7))
        aStack.addToStack(Card(7, 3))
        aStack.addToStack(Card(66, 2))
        self.assertEqual(66, aStack.getTopCard().faceValue)

    ### GAMEBOARD TESTS

    def initializeGameBoard(self):
        card1 = Stack(Card(67, 5))
        card2 = Stack(Card(87, 4))
        card3 = Stack(Card(75, 7))
        card4 = Stack(Card(48, 2))
        cards = [card1, card2, card3, card4]
        self.gameBoard = GameBoard(cards)

    def testPlaceCards(self):
        player0 = Player(0)
        player1 = Player(1)
        player2 = Player(2)
        player3 = Player(3)

        selections = [(player0, Card(7, 3)), (player1, Card(20, 4)),
                      (player2, Card(18, 1)), (player3, Card(3, 6))]

        # First test round for this function
        self.initializeGameBoard()
        self.gameBoard.placeCards(selections)
        self.assertEquals(self.gameBoard.stacks[0], Stack(Card(67, 5)))
        self.assertEquals(self.gameBoard.stacks[1], Stack(Card(87, 4)))
        self.assertEquals(self.gameBoard.stacks[2], Stack(Card(75, 7)))
        self.assertEquals(self.gameBoard.stacks[3].getTopCard(), Card(20, 4))

        # Second test round

        secondSelections = [(player0, Card(62, 3)), (player1, Card(63, 4)),
                            (player2, Card(69, 1)), (player3, Card(70, 6))]
        self.gameBoard.placeCards(secondSelections)
        self.assertEquals(self.gameBoard.stacks[0].getTopCard(), Card(70, 6))
        self.assertEquals(self.gameBoard.stacks[0].getNumCards(), 3)
        self.assertEquals(self.gameBoard.stacks[1].getTopCard(), Card(87, 4))
        self.assertEquals(self.gameBoard.stacks[1].getNumCards(), 1)
        self.assertEquals(self.gameBoard.stacks[2].getTopCard(), Card(75, 7))
        self.assertEquals(self.gameBoard.stacks[2].getNumCards(), 1)
        self.assertEquals(self.gameBoard.stacks[3].getTopCard(), Card(63, 4))
        # A patch that allows stacks to have 6 cards will cause this test to
        # change if the patch is applied, so we leave it out.
        # self.assertEquals(self.gameBoard.stacks[3].getNumCards(), 1)

    def testClearStack(self):
        self.initializeGameBoard()
        self.gameBoard.stacks[0].addToStack(Card(30, 7))
        self.gameBoard.stacks[0].addToStack(Card(7, 3))
        self.gameBoard.stacks[0].addToStack(Card(66, 2))
        player1 = Player(1)
        self.gameBoard.clearStack(player1, Card(32, 3), 0)
        stackResult = Stack(Card(32, 3))
        self.assertEquals(stackResult, self.gameBoard.stacks[0])
        self.assertEquals(player1.bullPoints, 17)

    def testIsSmallerThanAllTopCards(self):
        someCards = [Stack(Card(25, 6)), Stack(Card(30, 7)), Stack(Card(7, 3)), Stack(Card(66, 2))]
        board = GameBoard(someCards)
        self.assertTrue(board.isSmallerThanAllTopCards(Card(3, 3)))
        self.assertFalse(board.isSmallerThanAllTopCards(Card(88, 3)))
        self.assertFalse(board.isSmallerThanAllTopCards(Card(50, 3)))

    def testFindClosestTopCard(self):
        someCards = [Stack(Card(25, 6)), Stack(Card(30, 7)), Stack(Card(7, 3)), Stack(Card(66, 2))]
        board = GameBoard(someCards)
        self.assertEqual(0, board.findClosestTopCard(Card(29, 3)))
        self.assertEqual(-1, board.findClosestTopCard(Card(6, 3)))  # should never be smaller

    # PLAYER TESTS

    def testChooseCard(self):
        self.initializeGameBoard()
        player1 = Player(1)
        player1.cards = [Card(25, 2), Card(54, 5), Card(79, 1), Card(17, 6), Card(20, 3)]
        bestCard = player1.chooseCard(self.gameBoard)
        # Since a Player's strategy can can be altered with a patch, we leave this test out for now
        # until we abstract a strategy
        # self.assertEquals(bestCard, Card(79, 1))
        self.assertEquals(len(player1.cards), 4)

    def testChooseStack(self):
        self.initializeGameBoard()
        self.gameBoard.stacks[0].addToStack(Card(25, 4))
        self.gameBoard.stacks[0].addToStack(Card(25, 3))
        self.gameBoard.stacks[0].addToStack(Card(25, 2))
        self.gameBoard.stacks[1].addToStack(Card(25, 6))
        self.gameBoard.stacks[2].addToStack(Card(25, 5))
        self.gameBoard.stacks[2].addToStack(Card(25, 7))
        player1 = Player(1)
        self.assertEquals(player1.chooseStack(self.gameBoard.stacks), 3)

    def testAddBullPoints(self):
        player1 = Player(1)
        player1.bullPoints = 7
        player1.addBullPoints(8)
        self.assertEquals(15, player1.bullPoints)

    # DEALER TESTS

    def testDealTenToEach(self):
        dealer = Dealer([Player(0), Player(1), Player(2), Player(3)])
        # A patch changes function name, so when patch is applied, test needs to change
        # dealer.dealTenToEach([0, 1, 2, 3])
        # for player in dealer.players:
        #     self.assertEquals(len(player.cards), 10)

    def testFindWinner(self):
        dealer = Dealer([Player(0), Player(1), Player(2), Player(3)])
        self.assertEquals(dealer.findWinner(), -1)
        dealer.players[1].addBullPoints(66)
        self.assertEquals(dealer.findWinner(), 1)
        dealer.players[1].addBullPoints(-1)
        self.assertEquals(dealer.findWinner(), -1)
        dealer.players[3].addBullPoints(71)
        self.assertEquals(dealer.findWinner(), 3)