# An internal Player in a game of Evolution
from species import *
from drawing import Drawing 
from traitCard import *
from sillyPlayer import SillyPlayer



class PlayerState:
	num = 0
	foodbag = 0
	species = []
	hand = []

	""" 
		Internal representation of a json player
		@param num: ID number
		@param foodbag: yep
		@param species: this player's species boards
		@param hand: traitcards in this player's hand (not on boards/haven't been traded in)
		@param player: the external player with strategic functionality
		Nat, Nat, ListOf(Species), ListOf(TraitCard), Player -> PlayerState
	"""
	def __init__(self, id, bag, speciesList, cards, player=None):
		self.num = id
		self.foodbag = bag
		self.species = speciesList
		self.hand = cards
		self.player = SillyPlayer()

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
		create dictionary 
		None -> Dict
	"""
	def toDict(self):
		return {"num": self.num, 
				"species": [species.toDict() for species in self.species], 
				"hand": [card.toDict() for card in self.hand], 
				"foodbag": self.foodbag}

	"""
		Display the essence of a player
		Void -> Void
	"""
	def display(self):
		Drawing(player=self.toDict())

	""" 
	   creates a json array of a PlayerState object
	   Void -> JsonArray
	"""
	def playerStateToJson(self):
		species = [Species.speciesToJson(animal) for animal in self.species]
		cards = [TraitCard.traitCardToJson(card) for card in self.hand]

		result = [["id", self.num],
				  ["species", species],
				  ["bag", self.foodbag]]

		if cards:
			result.append(["cards", cards])

		return result

	"""
	   creates a PlayerState from a json array
	   JsonArray -> PlayerState
	"""
	@staticmethod
	def playerStateFromJson(state):
		try:
			cards = []
			if state[0][0] == "id":
				num = state[0][1]
			if state[1][0] == "species":
				speciesList = [Species.speciesFromJson(species) for species in state[1][1]]
			if state[2][0] == "bag":
				bag = state[2][1]
			if len(state) == 4 and state[3][0] == "cards":
				cards = [TraitCard.traitCardFromJson(card) for card in state[3][1]]
			if num > 0 and bag >= 0:
				return PlayerState(num, bag, speciesList, cards)

		except:
			quit()

	"""
		Proxy to call the feed method in the external player
		@param wateringHole: the amount of food that can be eaten
		@param players: all the players in this round
		@return FeedingAction -One of:
			False - no feeding at this time
			Nat - index of Species fed
			[Nat, Nat] - index of fat-tissue Species fed, amount of fatFood
			[Nat, Nat, Nat] - index of carnivore, index of player to attack, index of species to attack
		Nat, ListOf(PlayerState) -> FeedingAction
	"""
	def feed(self, wateringHole, player):
		return self.player.feed(self, wateringHole, player)

	"""
		Filter out all fed species to get a list of species that can be fed
		@return a list of (Species' index, Species) for hungry species this player has
		Void -> ListOf((Nat, Species))
	"""
	def getHungrySpecies(self):
		hungry = []
		for i in range(len(self.species)):
			if self.species[i].isHungry():
				hungry.append((i, self.species[i]))

		return hungry

	"""
		Gets the indexes of the species neighboring the given species
		@param speciesIdx: index of the species to get neighbors for
		Nat -> [OptSpecies, OptSpecies] where an OptSpecies is Species or False
	"""
	def getNeighbors(self, speciesIdx):
		if speciesIdx > 0:
			lNeighbor = self.species[speciesIdx - 1]
		else:
			lNeighbor = False

		if speciesIdx < len(self.species) - 1:
			rNeighbor = self.species[speciesIdx + 1]
		else:
			rNeighbor = False

		return [lNeighbor, rNeighbor]

	"""
		Verify that this player can use their own chosen species to attack the other given species
		@param defPlayer: PlayerState of the defending player
		@param defIdx: index of the defending species
		@param attIdx: index of the attacking species: should be one of our own
		PlayerState, Nat, Nat -> Boolean
	"""
	def verifyAttack(self, defPlayer, attIdx, defIdx):
		left, right = defPlayer.getNeighbors(defIdx)
		return Species.isAttackable(defPlayer.species[defIdx], self.species[attIdx], left, right)

	"""
		Tell whether or not the given species is extinct (i.e. that its population <= 0)
		@param specIdx: index of the species to check
		Nat -> Boolean
	"""
	def isExtinct(self, specIdx):
		return self.species[specIdx].isExtinct()

	"""
		Remove the given species from this player's list of species
		@param specIdx: index of the species to remove
		Nat -> Void
	"""
	def removeSpecies(self, specIdx):
		del self.species[specIdx]

	"""
		Tell whether or not this player has any species
		Void -> Boolean
	"""
	def hasNoSpecies(self):
		return not (len(self.species) > 0)

	"""
		Tell whether the species at the given index has the given trait
		@param specIdx: the index of the species to check
		@param traitName: the name of the trait to check for
		Nat, String -> Boolean
	"""
	def speciesHasTrait(self, specIdx, traitName):
		return self.species[specIdx].hasTrait(traitName)

	"""
		Drop the population of the given species as in a carnivore attack
		If the species' food > its population, drop the food as well
		@param specIdx: the index of the species to have its population decremented
		Nat -> Void
	"""
	def executeAttack(self, specIdx):
		self.species[specIdx].executeAttack()

	"""
		Feed the given species the given amount of fat food that it requested
		@param specIdx: index of the species to feed
		@param foodCount: amount of food to try to feed
		@return the amount of food this species was given
		Nat, Nat -> Nat
	"""
	def feedFatFood(self, specIdx, foodCount):
		spec = self.species[specIdx]
		if spec.hasTrait("fat-tissue"):
			foodCount = min(foodCount, spec.body - spec.fatFood)
			spec.eatFatFood(foodCount)
			return foodCount
		else:
			raise ValueError("Tried to feed fat food to a species without fat tissue")

	"""
		Feed a given species the amount of food that it requested
		@param specIdx: index of the species to feed
		@param foodCount: amount of food to try to feed
		@param wateringHole: the amount of food in the dealer's watering hole
		@return the total amount of food eaten during this feeding
		Nat, Nat, Nat -> Nat
	"""
	def feedSpecies(self, specIdx, foodCount, wateringHole):
		spec = self.species[specIdx]
		foodCount = min(wateringHole, foodCount, spec.population - spec.food)
		spec.eatFood(foodCount)
		wateringHole -= foodCount

		forageAmount = self.forage(specIdx, wateringHole)
		wateringHole -= forageAmount
		foodCount += forageAmount
		
		foodCount += self.cooperate(specIdx, foodCount, wateringHole)

		return foodCount

	"""
		If the given species has the foraging trait, give it one more food
		@param specIdx: index of the species to feed
		@param wateringHole: the amount of food in the dealer's watering hole
		@return the amount of food this species ate
	"""
	def forage(self, specIdx, wateringHole):
		spec = self.species[specIdx]
		amountFed = 0
		if wateringHole > 0 and spec.hasTrait("foraging") and spec.population > spec.food:
			spec.eatFood(1)
			amountFed += 1

		return amountFed

	"""
		Cooperate
		@param specIdx: index of the species to feed
		@param foodCount: amount of food to try to feed
		@param wateringHole: the amount of food in the dealer's watering hole
		@return the amount of food all species in the cooperation chain ate
		Nat, Nat, Nat -> Nat
	"""
	def cooperate(self, specIdx, foodCount, wateringHole):
		spec = self.species[specIdx]
		amountFed = 0
		left, right = self.getNeighbors(specIdx)
		if spec.hasTrait("cooperation") and right is not False:
			for i in range(foodCount):
				if wateringHole > 0:
					fedThisSpecies = self.feedSpecies(specIdx+1, 1, wateringHole)
					amountFed += fedThisSpecies
					wateringHole -= fedThisSpecies

		return amountFed

	"""
		After a carnivore attack, have all species with the scavenge trait eat from left to right
		@param wateringHole: the amount of food that can be handed out amongst the scavengers
		@return the amount of food eaten amongst our scavengers
		Nat -> Nat
	"""
	def scavenge(self, wateringHole):
		amountFed = 0
		for i in range(len(self.species)):
			if self.speciesHasTrait(i, "scavenger"):
				fedThisSpecies = self.feedSpecies(i, 1, wateringHole)
				amountFed += fedThisSpecies
				wateringHole -= fedThisSpecies

		return amountFed

