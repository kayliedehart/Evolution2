from traitCard import TraitCard
from species import Species
from playerState import PlayerState

"""
All methods in this class process to and from arrays that can be dumped/loaded in json
However, actual calls to json.dump/load should be made in proxy classes, as they are
not done here
"""
class JsonParsing:

    ############ FOR SPECIES

    """
        creates a json array fitting the spec from the given species
        Species -> JsonArray
    """
    @staticmethod
    def speciesToJson(species):	
        if species is False:
            return False

        result = [["food", species.food],
                  ["body", species.body],
                  ["population", species.population],
                  ["traits", [trait.name for trait in species.traits]]]

        if species.fatFood > 0:
            result.append(["fat-food", species.fatFood])

        return result

    """ 
       Helper to convert json species to internal Species
       JSONSpecies = [["food",Nat],
       ["body",Nat],
       ["population",Nat],
       ["traits",LOT],
       OPT: ["fat-food",Nat]]
       JSONSpecies -> OptSpecies
       TODO: make this like playerState where it errors out
    """
    @staticmethod
    def speciesFromJson(jsonSpecies):    
        # If the if statement errors out, the input is ill shaped
        try:
        	if jsonSpecies is False:
        		return False

                if jsonSpecies[0][0] == "food" and jsonSpecies[1][0] == "body" and jsonSpecies[2][0] == "population" and jsonSpecies[3][0] == "traits":
                    food = jsonSpecies[0][1]
                    body = jsonSpecies[1][1]
                    population = jsonSpecies[2][1]
                    traits = []
                    hasFatTissue = False

                    for trait in jsonSpecies[3][1]:
                        if trait == "fat-tissue":
                            hasFatTissue = True
                        traits.append(TraitCard(trait))

                    if len(jsonSpecies) == 5 and hasFatTissue and jsonSpecies[4][0] == "fat-food":
                        fatFood = jsonSpecies[4][1]
                    else:
                        fatFood = 0

                    return Species(food, body, population, traits, fatFood)
                else:
                    pass
                    # TODO: what should actually happen when the labels for an array are wrong?

        except Exception as e:
            raise e


    """ 
       convert a json species from spec to a list of species/optspecies
       JsonSituation -> [Species, Species, OptSpecies, OptSpecies]
    """
    @staticmethod
    def situationFromJson(situation):    
        defend = JsonParsing.speciesFromJson(situation[0])
        attack = JsonParsing.speciesFromJson(situation[1])

        if not attack or not defend:
            quit()

        lNeighbor = JsonParsing.speciesFromJson(situation[2]) or Species(0, 0, 0, [])
        rNeighbor = JsonParsing.speciesFromJson(situation[3]) or Species(0, 0, 0, [])

        return defend, attack, lNeighbor, rNeighbor



	########### FOR PLAYERSTATE

    """ 
       creates a json array of a PlayerState object
       PlayerState -> JsonArray
    """
    @staticmethod
    def playerStateToJson(state):
        species = []
        for animal in state.species:
            species.append(JsonParsing.speciesToJson(animal))

        return [["id", state.num],
                ["species", species],
                ["bag", state.foodbag]]

    """
       creates a PlayerState from a json array
       JsonArray -> PlayerState
       TODO: make this not quite so awful
       for one: what should happen in the else cases?
    """
    @staticmethod
    def playerStateFromJson(state):
        id = 0
        bag = -1
        speciesList = []

        try:
            if state[0][0] == "id":
                id = state[0][1]

            if state[1][0] == "species":
                for species in state[1][1]:
                    speciesList.append(JsonParsing.speciesFromJson(species))

            if state[2][0] == "bag":
                bag = state[2][1]

            if id > 0 and bag >= 0:
                return PlayerState(id, bag, speciesList)

        except Exception as e:
            raise e

