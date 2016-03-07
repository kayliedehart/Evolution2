from species import *


class PlayerState:

    # Internal representation of a json player
    # TODO: fix mutable lists
    # Opts: Nat, Nat, ListOf(Species), ListOf(TraitCard) -> PlayerState
    def __init__(self, id=0, bag=0, speciesList=[], cards=[]):
        self.num = id
        self.foodbag = bag
        self.species = speciesList
        self.hand = cards

    """ 
        override equality
        Any -> Boolean
    """
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    """ 
        override inequality
        Any -> Boolean
    """
    def __ne__(self, other):
        return not self.__eq__(other)