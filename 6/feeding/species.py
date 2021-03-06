import constants

class Species:

    def __init__(self, food=0, body=0, population=1, traits=[], fatFood=0):
        self.food = food
        self.body = body
        self.population = population
        self.traits = traits
        self.fatFood = fatFood

    # Sets food points for this species
    # Nat -> void
    def setFoodPoints(self, numFood):
        self.food = numFood

    # Sets body size for this species
    # Nat -> void
    def setBody(self, bodySize):
        self.body = bodySize

    # Sets a list of traits for this species
    # Size should be no more than 3
    # listOf(Trait) -> void
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
        if "fat-tissue" not in self.traits:
            raise ValueError("Can't store food without fat tissue trait")
        if (food > self.body):
            raise ValueError("Can't have more stored food than body size")

        self.fatFood = food

    # Determine if this species is larger than the given one
    # THIS SHOULD BE CALLED ON THE NEW/CANDIDATE SPECIES
    # aka if there are two possible things to attack and you already chose one as a possibility,
    # call newPossibility.isLarger(oldPossibility)
    # OptSpecies (aka Species or Boolean) -> Boolean
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
    # OptSpecies -> Boolean
    def isSameSize(self, that):
        if not that:
            return False
        else:
            return self.population == that.population and self.body == that.body and self.food == that.food


    # creates a json array fitting the spec from the given species
    def toJsonArray(self):
        result = [["food", self.food],
                ["body", self.body],
                ["population", self.population],
                ["traits", self.traits]]

        if self.fatFood > 0:
            result.append(["fat-food", self.fatFood])

        return result

    # helper to convert json
    # Situation -> [Species, Species, OptSpecies, OptSpecies]
    @staticmethod
    def jsonToSituation(situation):
        defend = Species.convertSpecies(situation[0])
        attack = Species.convertSpecies(situation[1])

        if not attack or not defend:
            quit()

        lNeighbor = Species.convertSpecies(situation[2]) or Species(0, 0, 0, [])
        rNeighbor = Species.convertSpecies(situation[3]) or Species(0, 0, 0, [])

        return defend, attack, lNeighbor, rNeighbor

    # Helper to convert json species to our data representation
    # JSONSpecies = [["food",Nat],
    #                ["body",Nat],
    #                ["population",Nat],
    #                ["traits",LOT],
    #           OPT: ["fat-food",Nat]]
    # JSONSpecies -> OptSpecies
    @staticmethod
    def convertSpecies(jsonSpecies):
        # If the if statement errors out, the input is ill shaped
        try:
            if jsonSpecies[0][0] == "food" and jsonSpecies[1][0] == "body" and \
                    jsonSpecies[2][0] == "population" and jsonSpecies[3][0] == "traits":
                food = jsonSpecies[0][1]
                body = jsonSpecies[1][1]
                population = jsonSpecies[2][1]
                traits = jsonSpecies[3][1]
                if len(jsonSpecies) == 5 and "fat-tissue" in traits and jsonSpecies[4][0] == "fat-food":
                    fatFood = jsonSpecies[4][1]
                else:
                    fatFood = 0
                return Species(food, body, population, traits, fatFood)

            else:
                return False

        except:
            return False


    # Given array of [defender, attacker, leftNeighbor, rightNeighbor], is the defender attackable?
    # listOf(Species) -> Boolean
    @staticmethod
    def isAttackable(defend, attack, lNeighbor, rNeighbor):
        if not lNeighbor:
            lNeighbor = Species(population=0)
        if not rNeighbor:
            rNeighbor = Species(population=0)

        if "carnivore" not in attack.traits:
            return False

        if defend.population != 0:

            if "warning-call" in lNeighbor.traits or "warning-call" in rNeighbor.traits:
                if "ambush" not in attack.traits:
                    return False

            if "burrowing" in defend.traits:
                if defend.food == defend.population:
                    return False

            if "climbing" in defend.traits:
                if "climbing" not in attack.traits:
                    return False

            if "hard-shell" in defend.traits:
                attackBody = attack.body
                if "pack-hunting" in attack.traits:
                    attackBody += attack.population
                if attackBody - defend.body < 4:
                    return False

            if "herding" in defend.traits:
                attackPopulation = attack.population
                if "horns" in defend.traits:
                    attackPopulation -= 1
                if attackPopulation - defend.population <= 0:
                    return False

            if "symbiosis" in defend.traits:
                if rNeighbor.body > defend.body:
                    return False

        return True
