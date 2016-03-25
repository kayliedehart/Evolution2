from species import *
from drawing import Drawing 


class PlayerState:
	num = 0
	foodbag = 0
	species = []
	hand = []

	""" 
		Internal representation of a json player
		num: ID number
		foodbag: yep
		species: this player's species boards
		hand: traitcards in this player's hand (not on boards/haven't been traded in)
		Nat, Nat, ListOf(Species), ListOf(TraitCard) -> PlayerState
	"""
	def __init__(self, id, bag, speciesList, cards):
		self.num = id
		self.foodbag = bag
		self.species = speciesList
		self.hand = cards

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
		Display the essence of a player
		Void -> Void
	"""
	def display(self):
		Drawing(player=self)

	"""
		Filter out all fed species to get a list of species that can be fed
		@return a list of (Species' index, Species) for hungry species this player has
		Void -> ListOf((Nat, Species))
	"""
	def getHungrySpecies(self):
		hungry = []
		for i in range(len(self.species)):
			s = self.species[i]
			if s.population > s.food or (s.body > s.fatFood and s.hasTrait("fat-tissue")):
				hungry.append((i, s))

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
			spec.fatFood += foodCount
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
		spec.food += foodCount
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
			spec.food += 1
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
