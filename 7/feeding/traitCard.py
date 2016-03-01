class TraitCard():

    # create a new trait card
    # String, Opt: Nat -> TraitCard
    def __init__(self, name, food=0):
        self.name = name
        self.food = food

    # check if two trait cards are equal
    # Any -> Boolean
    def __eq__(self, that):
        if isinstance(that, TraitCard):
            return self.name == that.name and self.food == that.food
        else:
            return False