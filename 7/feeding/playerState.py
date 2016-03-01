from species import *


class PlayerState:

    # Internal representation of a json player
    # Opts: Nat, Nat, ListOf(Species), ListOf(Trait) -> PlayerState
    def __init__(self, id=0, bag=0, speciesList=[], traits=[]):
        self.num = id
        self.foodbag = bag
        self.species = speciesList
        self.traits = traits

    # creates a json array from this object
    # Void -> JsonArray
    def toJsonArray(self):
        species = []
        for animal in self.species:
            species.append(animal.toJsonArray())
        return [["id", self.num],
                ["species", species],
                ["bag", self.foodbag]]

    # creates a PlayerState from a json array
    # JsonArray -> PlayerState
    @staticmethod
    def convertPlayerState(state):
        id = 0
        bag = -1
        speciesList = []
        try:
            if state[0][0] == "id" and state:
                id = state[0][1]
            # assumes a jsonArray species
            if state[1][0] == "species":
                for species in state[1][1]:
                    speciesList.append(Species.convertSpecies(species))
            if state[2][0] == "bag":
                bag = state[2][1]

            if id > 0 and bag >= 0:
                return PlayerState(id, bag, speciesList)

        except Exception as e:
            raise e
