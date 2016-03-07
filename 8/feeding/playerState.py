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
