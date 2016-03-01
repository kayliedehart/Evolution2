from Stack import *


class GameBoard:

    # creates an initial GameBoard state with the given four stack starters
    # __init__: ArrayOfStack -> GameBoard
    def __init__(self, stackCards):
        self.stacks = stackCards

    # performs the move that the player wants to make
    # will allocate bullpoints if the player gains any from this move
    # placeCard: ListOf(Tuple(Player, Card)) -> Void
    def placeCards(self, selections):
        # place cards in ascending order, clear stacks when necessary,
        # and allocate points to their player if gained/lost
        selections.sort(key=lambda tup: tup[1].faceValue)
        for player, card in selections:
            if self.isSmallerThanAllTopCards(card):
                idxToClear = player.chooseStack(self.stacks)
                self.clearStack(player, card, idxToClear)
            else:
                stackIdx = self.findClosestTopCard(card)  # Return stack index
                if self.stacks[stackIdx].getNumCards() == 5:
                    self.clearStack(player, card, stackIdx)
                else:
                    self.stacks[stackIdx].cards.append(card)

    # clearStack: Player, Card, Nat -> Void
    def clearStack(self, player, card, stackIdx):
        player.addBullPoints(self.stacks[stackIdx].getBullPoints())
        self.stacks[stackIdx] = Stack(card)

    # isSmallerThanAllTopCards: Card -> Boolean
    def isSmallerThanAllTopCards(self, card):
        smaller = True
        for stack in self.stacks:
            topCard = stack.getTopCard()
            smaller = smaller and (card.faceValue < topCard.faceValue)

        return smaller

    # this should only be called when we're sure there are smaller cards
    # findClosestTopCard: Card -> Nat
    def findClosestTopCard(self, card):
        idx = -1
        diff = float('inf')
        for i in range(4):
            topFace = self.stacks[i].getTopCard().faceValue
            if topFace < card.faceValue and card.faceValue - topFace < diff:
                idx = i
                diff = card.faceValue - topFace

        return idx

