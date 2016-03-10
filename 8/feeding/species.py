import constants
from traitCard import *


class Species:
    food = 0
    body = 0
    population = 1
    traits = []
    fatFood = 0

    """ 
        creates a Species
        food: how much food this species has eaten this turn
        body: body size
        population: population size
        traits: trait cards on this species board (up to 3)
        fatFood: how much food has been stored on a fat tissue card
                 can only be non-zero when a fat tissue card is in self.traits
        Nat, Nat, Nat, ListOf(TraitCard), Nat -> Species
    """
    def __init__(self, food, body, population, traits, fatFood):
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

    """ 
        tell if this species has a trait card with a certain name
        String -> Boolean
    """
    def hasTrait(self, name):
        for trait in self.traits:
            if trait.name == name:
                return True

        return False

    """ 
        Determine if this species is larger than the given one
        THIS SHOULD BE CALLED ON THE NEW/CANDIDATE SPECIES
        aka if there are two possible things to attack and you already chose one as a possibility,
        call newPossibility.isLarger(oldPossibility)
        this is to enforce the invariant of order of species boards being a tie-breaker
        OptSpecies (one of Species or Boolean) -> Boolean
    """
    def isLarger(self, that):
        if not that:
            return True

        if self.population == that.population and self.food == that.food:
            return self.body > that.body
        elif self.population == that.population:
            return self.food > that.food
        else:
            return self.population > that.population

    """
        tells if these two have the same size
        OptSpecies (one of Species or Boolean) -> Boolean
    """
    def isSameSize(self, that):
        if not that:
            return False
        else:
            return self.population == that.population and self.body == that.body and self.food == that.food


    """
        Given array of [defender, attacker, leftNeighbor, rightNeighbor], is the defender attackable?
        TODO: restate spec here
        Species, Species, OptSpecies (one of Boolean or Species), OptSpecies -> Boolean
    """
    @staticmethod
    def isAttackable(defend, attack, lNeighbor, rNeighbor):
        if not lNeighbor:
            lNeighbor = Species(0, 0, 0, [], 0)
        if not rNeighbor:
            rNeighbor = Species(0, 0, 0, [], 0)

        if not attack.hasTrait("carnivore"):
            return False

        if defend.population != 0:
            if lNeighbor.hasTrait("warning-call") or rNeighbor.hasTrait("warning-call"):
                if not attack.hasTrait("ambush"):
                    return False

            if defend.hasTrait("burrowing"):
                if defend.food == defend.population:
                    return False

            if defend.hasTrait("climbing"):
                if not attack.hasTrait("climbing"):
                    return False

            if defend.hasTrait("hard-shell"):
                attackBody = attack.body
                if attack.hasTrait("pack-hunting"):
                    attackBody += attack.population
                if attackBody - defend.body < 4:
                    return False

            if defend.hasTrait("herding"):
                attackPopulation = attack.population
                if defend.hasTrait("horns"):
                    attackPopulation -= 1
                if attackPopulation - defend.population <= 0:
                    return False

            if defend.hasTrait("symbiosis"):
                if rNeighbor.body > defend.body:
                    return False

        return True
