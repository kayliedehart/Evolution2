class Stack:

    # creates a new stack with the given card at the head
    # __init__: Card -> Stack
    def __init__(self, card):
        self.cards = []
        self.addToStack(card)

    # addToStack: Card -> Void
    def addToStack(self, card):
        self.cards.append(card)

    # getBullPoints: Void -> Nat
    def getBullPoints(self):
        totalBullPoints = 0
        for card in self.cards:
            totalBullPoints += card.bullPoints
        return totalBullPoints

    # getNumCards: Void -> Nat
    def getNumCards(self):
        return len(self.cards)

    # getTopCard: Void -> Card
    def getTopCard(self):
        return self.cards[len(self.cards) - 1]

    # Override str to make readable Stack printouts
    def __str__(self):
        result = ""
        for card in self.cards:
            result += str(card) + " "
        return result

    #Override eq to make Stacks with same Cards in same spots equal
    def __eq__(self, other):
        if isinstance(other, Stack):
            for i in range(len(self.cards)):
                if not self.cards[i] == other.cards[i]:
                    return False
            return True

        return False

