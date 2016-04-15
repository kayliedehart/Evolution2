# An external Player strategy implementation
from species import *
from action4 import Action4
from buySpeciesBoard import BuySpeciesBoard
from replaceTrait import ReplaceTrait
from gainPopulation import GainPopulation
from gainBodySize import GainBodySize


class SillyPlayer:
	# Current PlayerState that corresponds to this player
	# Supplied in start()
	state = False


	def __init__(self):
		self.state = False


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
		Get our own state at the end of step 1 of a game (new species/cards added)
		SillyPlayer does nothing with this
		@param curState: PlayerState representing us
		PlayerState -> Void
	"""
	def start(self, curState):
		self.state = curState

	"""
		Choose an action for steps 2 and 3 of the game
		SillyPlayer just picks the biggest cards in order
		@param befores: all the species of players who went before this one
		@param afters: all the species of players who go before this one
		@return the card to place at the watering hole and what trades to make
		ListOf(ListOf(Species)), ListOf(ListOf(Species)) -> Action4
	"""
	def choose(self, befores, afters):
		cardsWIdx = [(i, self.state.hand[i]) for i in range(len(self.state.hand))]
		cards = sorted(cardsWIdx, key=lambda x: x[1], cmp=TraitCard.compare) 
		maxCardIdx = len(cards) - 1
		newSpecIdx = len(self.state.species)
		curCardIdx = 3
		
		gp = [GainPopulation(newSpecIdx, cards[curCardIdx][0])] if curCardIdx <= maxCardIdx else []
		curCardIdx += 1
		gb = [GainBodySize(newSpecIdx, cards[curCardIdx][0])] if curCardIdx <= maxCardIdx else []
		curCardIdx += 1
		rt = [ReplaceTrait(newSpecIdx, 0, cards[curCardIdx][0])] if curCardIdx <= maxCardIdx else []

		return Action4(cards[0][0], gp, gb, [BuySpeciesBoard(cards[1][0], [cards[2][0]])], rt) 
		
	"""
		Sorts a list of species from largest to smallest, giving precedence to population, then food eaten, then body size
		@param species: a tuple of (the original index the species was at when given by the dealer, species object)
		@return the same tuples sorted with the largest species first
		listOf(Tuple(Nat, Species)) -> listOf(Tuple(Nat, Species))
	"""
	@staticmethod
	def sortSpecies(species):
		result = []
		for i, s in species:
			if s.isHungry():
				result.append((i, s))

		result = sorted(result, key=lambda x: (x[1].population, x[1].food, x[1].body), reverse=True)
		return result

	"""
		Gets a fat tissue species with the greatest need and its current needs
		@param species: the list of species to choose from
		@param wateringHole: the max. amount of food that can be taken
		@return the index of the species to be fed and the amount it wants to eat
		ListOf((Nat, Species)), Nat -> Nat or False, Nat or False
	"""
	@staticmethod
	def getFatTissueSpecies(species, wateringHole):
		speciesIndex = False
		currentNeed = 0
		for i, animal in species:
			if animal.hasTrait("fat-tissue") and animal.body > animal.fatFood:
				animalNeed = animal.body - animal.fatFood
				if speciesIndex is False or animalNeed > currentNeed:
					speciesIndex = i
					currentNeed = animalNeed

		return speciesIndex, min(currentNeed, wateringHole)

	"""
		Gets a vegetarian species with the greatest need
		Invariant: list is already ordered 
		ListOf(Tuple(Nat, Species)) -> Nat or False
	"""
	@staticmethod
	def getVegetarian(species):
		for index, animal in species:
			if not animal.hasTrait("carnivore") and animal.population > animal.food:
				return index

		return False

	""" 
		Gets an attacker and a player + species to attack
		ListOf(Tuple(Nat, Species)), ListOf(PlayerState) -> (Nat or False, Nat or False, Nat or False)
	"""
	@staticmethod
	def getCarnivoreAttack(species, otherPlayers):
		carnIndex = defPlayerIndex = preyIndex = False
		for i, animal in species:
			if animal.hasTrait("carnivore"):
				# get a player with an attackable animal
				for j in range(len(otherPlayers)):
					defender = otherPlayers[j]
					# get an attackable animal; range so that we can check bounds before getting neighbors
					for k in range(len(defender.species)):
						lNeighbor, rNeighbor = defender.getNeighbors(k)
						if (Species.isAttackable(defender.species[k], animal, lNeighbor, rNeighbor) 
											and	(preyIndex is False 
											  or (defender.species[k].compare(otherPlayers[defPlayerIndex].species[preyIndex])) > 0)):
							defPlayerIndex = j
							preyIndex = k
							carnIndex = i

		return carnIndex, defPlayerIndex, preyIndex

	"""
		Find the index of the given player in a list of players
		Invariant: players must have unique IDs
		@param curState: the state to find in the list
		@param players: the list of players, which may or may not contain curState
		@return the index of the player, or False if it is not in the list, and the list of players that aren't us
		PlayerState, ListOf(PlayerState) -> (Nat or False), ListOf(PlayerState)
	"""
	@staticmethod
	def getIndex(curState, players):
		otherPlayers = []
		myIndex = False
		for i in range(len(players)):
			if players[i].num != curState.num:
				otherPlayers.append(players[i])
			else:
				myIndex = i
		return [myIndex, otherPlayers]

	"""
		Take the given state's species, associate them with their original place in the list,
		and then sort the list
		@param curState: the state whose species we should sort
		@return a list of species with their original index sorted by size
		PlayerState -> ListOf((Nat, Species))
	"""
	@staticmethod
	def indexSpecies(curState):
		speciesWithIndices = []
		for i in range(len(curState.species)):
			speciesWithIndices.append((i, curState.species[i]))
		return SillyPlayer.sortSpecies(speciesWithIndices)

	"""
		Choose a species to feed
		@param curState: current public state of this player
		@param wateringHole: amount of food in wateringHole
		@param players: current public states of all players
		@return FeedingAction -One of:
			[Nat, Nat] - index of fat-tissue Species fed, amount of fatFood
			Nat - index of an herbivore Species fed
			[Nat, Nat, Nat] - index of carnivore, index of player to attack, index of species to attack
			False - no feeding at this time
		PlayerState, Nat, ListOf(PlayerState) -> FeedingAction
	"""
	@staticmethod
	def feed(curState, wateringHole, players):
		species = SillyPlayer.indexSpecies(curState)
		myIndex, otherPlayers = SillyPlayer.getIndex(curState, players)

		fatTissueSpecies, currentNeed = SillyPlayer.getFatTissueSpecies(species, wateringHole)
		vegetarian = SillyPlayer.getVegetarian(species)
		carnivore, defender, prey = SillyPlayer.getCarnivoreAttack(species, otherPlayers)

		if fatTissueSpecies is not False:
			return [fatTissueSpecies, currentNeed]
		elif vegetarian is not False:
			return vegetarian
		elif carnivore is not False:
			if myIndex is not False and defender >= myIndex:
				defender += 1 # account for our placement in the original given player list
			return [carnivore, defender, prey]
		else:
			return False
