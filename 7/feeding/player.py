from species import *


class Player:

    # create a new Player
    # Nat -> Player
    def __init__(self, num):
        self.playerNum = num

    # Sorts a list of species from largest to smallest using Species.isLarger
    # The first Nat in the tuple is the original index the species was at when given by the dealer
    # set removeFed to True if you would like to filter out all species that cannot be fed
    # listOf(Tuple(Nat, Species)), Opt: Boolean -> listOf(Tuple(Nat, Species))
    def sortSpecies(self, species, removeFed=False):
        result = species
        if removeFed:
            temp = []
            for i, s in species:
                if s.population > s.food or (s.body > s.fatFood and s.hasTrait(constants.FAT_TISSUE)):
                    temp.append((i, s))
            result = temp
        result = sorted(result, key=lambda x: (x[1].population, x[1].food, x[1].body), reverse=True)
        return result

    # Gets a fat tissue species with the greatest need and its current needs
    # ListOf((Nat, Species)), Nat -> Nat, Nat
    def getFatTissueSpecies(self, species, wateringHole):
        fatTissueSpecies = False
        speciesIndex = -1
        currentNeed = 0
        for i, animal in species:
            if animal.hasTrait(constants.FAT_TISSUE) and animal.body > animal.fatFood:
                if not fatTissueSpecies:
                    fatTissueSpecies = animal
                    speciesIndex = i
                    currentNeed = animal.body - animal.fatFood
                else:
                    animalNeed = animal.body - animal.fatFood
                    # in the case that they're equal, current already takes precedence because it was to the left
                    # of the animal we're checking (by list ordering)
                    if animalNeed > currentNeed:
                        fatTissueSpecies = animal
                        speciesIndex = i
                        currentNeed = animalNeed

        if currentNeed > wateringHole:
            currentNeed = wateringHole

        return speciesIndex, currentNeed

    # Gets a vegetarian species with the greatest need
    # ListOf(Tuple(Nat, Species)) -> Nat
    def getVegetarian(self, species):
        for index, animal in species:
            # Return the first hungry vegetarian in an already ordered list
            if not animal.hasTrait(constants.CARNIVORE) and animal.population > animal.food:
                return index

        return -1

    # Gets an attacker and a player + species to attack
    # ListOf(Tuple(Nat, Species)), ListOf(PlayerState) -> (Nat, Nat, Nat)
    def getCarnivoreAttack(self, species, otherPlayers):
        prey = False
        carnIndex = defPlayerIndex = preyIndex = -1

        for i, animal in species:
            if animal.hasTrait(constants.CARNIVORE):
                canAttack = False
                # get a player with an attackable animal
                for j in range(len(otherPlayers)):
                    defender = otherPlayers[j]
                    # get an attackable animal; range so that we can check bounds before getting neighbors
                    for k in range(len(defender.species)):
                        if k > 0:
                            lNeighbor = defender.species[k-1]
                        else:
                            lNeighbor = False

                        # -2 b/c last item in a list is len-1
                        if k < len(defender.species) - 2:
                            rNeighbor = defender.species[k+1]
                        else:
                            rNeighbor = False

                        if (Species.isAttackable(defender.species[k], animal, lNeighbor, rNeighbor) and
                                                                                defender.species[k].isLarger(prey)):
                            defPlayerIndex = j
                            prey = defender.species[k]
                            preyIndex = k
                            carnIndex = i
                            canAttack = True

                if canAttack:
                    return carnIndex, defPlayerIndex, preyIndex
                else:
                    return -1, -1, -1

    # Choose a species to feed
    # handed states of all players so strategic moves can be made based on neighbors
    # it will return a FeedingAction; see the FeedingAction class for more information
    # PlayerState, Nat, ListOf(PlayerState) -> FeedingAction
    def feed(self, curState, wateringHole, otherPlayers):
        speciesWithIndices = []

        for i in range(len(curState.species)):
            speciesWithIndices.append((i, curState.species[i]))
        species = self.sortSpecies(speciesWithIndices, removeFed=True)
        if not species:
            return False

        fatTissueSpecies, currentNeed = self.getFatTissueSpecies(species, wateringHole)
        if fatTissueSpecies != -1:
            return [fatTissueSpecies, currentNeed]

        vegetarian = self.getVegetarian(species)
        if vegetarian != -1 and wateringHole > 0:
            return vegetarian

        carnivore, defender, prey = self.getCarnivoreAttack(species, otherPlayers)
        if (carnivore, defender, prey) != (-1, -1, -1):
            return [carnivore, defender, prey]

        # none can be fed
        return False
