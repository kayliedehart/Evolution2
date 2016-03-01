from species import *
from feedingAction import *

class Player:

    # create a new Player
    # Nat -> Player
    def __init__(self, num):
        self.playerNum = num

    # Gets a fat tissue species with the greatest need and its current needs
    # ListOf(Species) -> Species, Nat
    def getFatTissueSpecies(self, species):
        fatTissueSpecies = False
        currentNeed = 0
        for animal in species:
            if "fat-tissue" in animal.traits and animal.body > animal.fatFood:
                if not fatTissueSpecies:
                    fatTissueSpecies = animal
                    currentNeed = animal.body - animal.fatFood
                else:
                    animalNeed = animal.body - animal.fatFood
                    # in the case that they're equal, current already takes precedence because it was to the left
                    # of the animal we're checking (by list ordering)
                    if animalNeed > currentNeed:
                        fatTissueSpecies = animal
                        currentNeed = animalNeed

        return fatTissueSpecies, currentNeed

    # Gets a vegetarian species with the greatest need
    # ListOf(Species) -> Species
    def getVegetarian(self, species):
        for animal in species:
            # Return the first hungry vegetarian in an already ordered list
            if "carnivore" not in animal.traits and animal.population > animal.food:
                return animal

        return False

    # Gets an attacker and a player + species to attack
    # ListOf(Species), ListOf(PlayerState) -> (Species, PlayerState, Species)
    def getCarnivoreAttack(self, species, otherPlayers):
        carnivore = defendingPlayer = prey = False
        currentNeed = 0

        # get the neediest feedable carnivore
        for animal in species:
            animalNeed = animal.population - animal.food
            if "carnivore" in animal.traits:
                if animalNeed > currentNeed or (animalNeed == currentNeed and animal.isLarger(carnivore)):
                    carnivore = animal
                    currentNeed = animalNeed

        canAttack = False
        # get a player with an attackable animal
        for defender in otherPlayers:
            # get an attackable animal; range so that we can check bounds before getting neighbors
            for i in range(len(defender.species)):
                if i > 0:
                    lNeighbor = defender.species[i-1]
                else:
                    lNeighbor = False

                # -2 b/c last item in a list is len-1
                if i < len(defender.species) - 2:
                    rNeighbor = defender.species[i+1]
                else:
                    rNeighbor = False

                if (Species.isAttackable(defender.species[i], carnivore, lNeighbor, rNeighbor) and
                                                                        defender.species[i].isLarger(prey)):
                    defendingPlayer = defender
                    prey = defender.species[i]
                    canAttack = True

        if canAttack:
            return carnivore, defendingPlayer, prey
        else:
            return False, False, False

    # Choose a species to feed
    # handed states of all players so strategic moves can be made based on neighbors
    # it will return a FeedingAction; see the FeedingAction class for more information
    # PlayerState, Nat, ListOf(PlayerState) -> FeedingAction
    def feed(self, curState, wateringHole, otherPlayers):

        species = curState.species
        fatTissueSpecies, currentNeed = self.getFatTissueSpecies(species)
        if fatTissueSpecies:
            return FeedingAction.createAction("fat-tissue", callerSpecies=fatTissueSpecies, tokens=currentNeed)

        vegetarian = self.getVegetarian(species)
        if vegetarian and wateringHole > 0:
            return FeedingAction.createAction("vegetarian", callerSpecies=vegetarian)

        carnivore, defender, prey = self.getCarnivoreAttack(species, otherPlayers)
        if carnivore and defender and prey:
            return FeedingAction.createAction("attack", callerSpecies=carnivore, defender=defender, prey=prey)

        # none can be fed
        return False