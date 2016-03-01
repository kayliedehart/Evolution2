from Deck import *
from GameBoard import *
import Constants


class Dealer:
    # leave empty to randomly generate
    bullPoints = Constants.BULL_POINTS
    cardsPerPlayer = Constants.CARDS_PER_PLAYER
    numStacks = Constants.NUM_STACKS

    def __init__(self, players):
        self.players = players
        self.board = []
        self.deck = Deck(self.bullPoints)

    # Keeps track of the players, manages rounds and turns,
    # and creates + returns the leaderboard
    # playGame: ArrayOfPlayer -> String
    def playGame(self):
        gameOver = False

        # runs rounds; will break when setting bullPoints <= 66 or 0 cards remain
        while not gameOver:
            # reset board, create four stacks
            self.deck = Deck(self.bullPoints)
            stackStarters = []
            for card in self.deck.cards[:self.numStacks]:
                stackStarters.append(Stack(card))
            self.deck.cards = self.deck.cards[self.numStacks:]
            self.board = GameBoard(stackStarters)

            # deal cards
            self.dealToEach()

            # run all turns in a round
            for i in range(self.cardsPerPlayer):
                cardsToPlay = []
                for player in self.players:
                    cardsToPlay.append((player, player.chooseCard(self.board)))

                self.board.placeCards(cardsToPlay)

                winnerIdx = self.findWinner()

                if winnerIdx >= 0:
                    gameOver = True

        self.printScoreBoard()

        return gameOver

    # deck is shuffled at generation time, so just deals first (numPlayers * cardsPerPlayer) cards
    # dealToEach: Void -> ArrayOfCard
    def dealToEach(self):
        numCardsToDeal = (self.cardsPerPlayer * len(self.players))
        if len(self.deck.cards) >= numCardsToDeal:
            cardsToDeal = self.deck.cards[:numCardsToDeal]
            self.deck.cards = self.deck.cards[numCardsToDeal:]
            for i in range(numCardsToDeal):
                # player index strictly corresponds to their number
                self.players[i % len(self.players)].cards.append(cardsToDeal[i])

    # check if anyone has over 66 bullpoints at the end of a turn
    # findWinner: Void -> Nat
    def findWinner(self):
        winnerIdx = -1
        for player in self.players:
            if player.bullPoints >= 66:
                winnerIdx = player.playerNum
                break

        return winnerIdx

    # print scoreboard to the terminal
    # printScoreBoard: Void -> Void
    def printScoreBoard(self):
        print("############### 6 NIMMT! ###############")
        print("+ PLAYER | BULLPOINTS +")
        self.players.sort(key=lambda player: player.bullPoints)
        for player in self.players:
            print("+ " + str(player.playerNum) + " | " + str(player.bullPoints) + " +")
        print("############### 6 NIMMT! ###############")

