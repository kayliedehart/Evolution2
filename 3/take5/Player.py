# Since we implemented a similar player interface for another team's Six Nimmt game with similar specifications,
# our code for this class will be similar to that of the other team's that we will be delivering

class Player:
    # defaults: invalid playerNum, most basic strategy,
    #           no bull points this round
    playerNum = -1
    strategy = 0
    bullPoints = 0

    # Creates a player by assigning it a number (and, if applicable, a strategy)
    # __init__:  Nat, [Optional: Nat] -> Player
    def __init__(self, playerNum, strategy=None):
        self.playerNum = playerNum
        self.cards = []

    # places a card in hand on board based on the defined strategy
    # Most basic strategy is to clear the stack with least amount of bull points
    # chooseCard: GameBoard -> Tuple(Card, Nat)
    def chooseCard(self, board):
        self.cards.sort(key=lambda tup: tup.faceValue)
        bestCard = self.cards[len(self.cards) - 1]
        del self.cards[-1]
        return bestCard

    # ADDED: OUR ORIGINAL SPECIFICATIONS LACKED THIS FUNCTION, BUT WE REALIZED THAT IT IS NEEDED FOR THIS PROJECT
    # chooses the stack with the lowest bullpoints to pick up
    # chooseStack: ListOf(Stacks) -> Nat
    def chooseStack(self, stacks):
        bestStackIndex = 0
        lowestStackBullPoints = float('inf')

        for i in range(len(stacks)):
            currentSum = sum(card.bullPoints for card in stacks[i].cards)
            if currentSum < lowestStackBullPoints:
                bestStackIndex = i
                lowestStackBullPoints = currentSum

        return bestStackIndex

    # addBullPoints: Nat -> Void
    def addBullPoints(self, n):
        self.bullPoints += n

