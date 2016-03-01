import random
import Constants
from Card import *


class Deck:
    numCards = Constants.NUM_CARDS

    # Creates a shuffled deck of numCards length,
    # with corresponding listOfBullPoints values
    # __init__: Nat, ListOf(Nat) -> Void
    def __init__(self, listOfBullPoints):
        self.cards = []
        # create a deck of Cards of this number of cards,
        # allocating the proper number of bullpoints to each
        if not listOfBullPoints:
            for i in range(self.numCards):
                listOfBullPoints.append(random.randint(Constants.MIN_BULLPOINTS, Constants.MAX_BULLPOINTS))

        for i in range(Constants.MIN_FACE_VALUE - 1, Constants.MAX_FACE_VALUE):
            self.cards.append(Card(i + 1, listOfBullPoints[i]))

        random.shuffle(self.cards)
