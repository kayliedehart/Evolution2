import constants
from traitCard import *


class Species:

    # creates a Species
    # TODO: fix mutable list
    # Opts: Nat, Nat, Nat, ListOf(TraitCard), Nat -> Species
    def __init__(self, food=0, body=0, population=1, traits=[], fatFood=0):
        self.food = food
        self.body = body
        self.population = population
        self.traits = traits
        self.fatFood = fatFood

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

    # Sets food points for this species
    # Nat -> void
    def setFoodPoints(self, numFood):
        self.food = numFood

    # Sets body size for this species
    # Nat -> void
    def setBody(self, bodySize):
        self.body = bodySize

    # Sets a list of traits for this species
    # Size should be no more than MAX_TRAITS
    # listOf(TraitCard) -> void
    def setTraits(self, traits):
        # range is not inclusive, hence +1
        if len(traits) not in range(0, constants.MAX_TRAITS + 1):
            raise ValueError("Number of traits should be between 0 and " + str(constants.MAX_TRAITS) + ", got " +
                                                                                                    str(len(traits)))
        self.traits = traits

    # Set the amount of fat food this species stores
    # Should not be settable when does not have fat tissue trait
    # Nat -> void
    def setFatFood(self, food):
        if not self.hasTrait(constants.FAT_TISSUE):
            raise ValueError("Can't store food without fat tissue trait")
        if food > self.body:
            raise ValueError("Can't have more stored food than body size")

        self.fatFood = food

    # tell if this species has a trait card with a certain name
    # String -> Boolean
    def hasTrait(self, name):
        for trait in self.traits:
            if trait.name == name:
                return True

        return False

    # Determine if this species is larger than the given one
    # THIS SHOULD BE CALLED ON THE NEW/CANDIDATE SPECIES
    # aka if there are two possible things to attack and you already chose one as a possibility,
    # call newPossibility.isLarger(oldPossibility)
    # this is to enforce the invariant of order of species boards being a tie-breaker
    # OptSpecies (one of Species or Boolean) -> Boolean
    def isLarger(self, that):
        if not that:
            return True

        if self.population == that.population and self.food == that.food:
            return self.body > that.body
        elif self.population == that.population:
            return self.food > that.food
        else:
            return self.population > that.population

    # tells if these two have the same size
    # OptSpecies (one of Species or Boolean) -> Boolean
    def isSameSize(self, that):
        if not that:
            return False
        else:
            return self.population == that.population and self.body == that.body and self.food == that.food


    # Given array of [defender, attacker, leftNeighbor, rightNeighbor], is the defender attackable?
    # Species, Species, OptSpecies (one of Boolean or Species), OptSpecies -> Boolean
    @staticmethod
    def isAttackable(defend, attack, lNeighbor, rNeighbor):
        if not lNeighbor:
            lNeighbor = Species(population=0)
        if not rNeighbor:
            rNeighbor = Species(population=0)

        if not attack.hasTrait(constants.CARNIVORE):
            return False

        if defend.population != 0:
            if lNeighbor.hasTrait(constants.WARNING_CALL) or rNeighbor.hasTrait(constants.WARNING_CALL):
                if not attack.hasTrait(constants.AMBUSH):
                    return False

            if defend.hasTrait(constants.BURROWING):
                if defend.food == defend.population:
                    return False

            if defend.hasTrait(constants.CLIMBING):
                if not attack.hasTrait(constants.CLIMBING):
                    return False

            if defend.hasTrait(constants.HARD_SHELL):
                attackBody = attack.body
                if attack.hasTrait(constants.PACK_HUNTING):
                    attackBody += attack.population
                if attackBody - defend.body < 4:
                    return False

            if defend.hasTrait(constants.HERDING):
                attackPopulation = attack.population
                if defend.hasTrait(constants.HORNS):
                    attackPopulation -= 1
                if attackPopulation - defend.population <= 0:
                    return False

            if defend.hasTrait(constants.SYMBIOSIS):
                if rNeighbor.body > defend.body:
                    return False

        return True
