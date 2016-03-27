from species import *


class SillyPlayer:

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
		@param species: the species to choose from
		@param wateringHole: the max. amount of food that can be taken
		@return the index of the species to be fed and the amount it wants to eat
		ListOf((Nat, Species)), Nat -> Nat, Nat
	"""
	@staticmethod
	def getFatTissueSpecies(species, wateringHole):
		fatTissueSpecies = False
		speciesIndex = -1
		currentNeed = 0
		for i, animal in species:
			if animal.hasTrait("fat-tissue") and animal.body > animal.fatFood:
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

	"""
		Gets a vegetarian species with the greatest need
		ListOf(Tuple(Nat, Species)) -> Nat
	"""
	@staticmethod
	def getVegetarian(species):
		for index, animal in species:
			# Return the first hungry vegetarian in an already ordered list
			if not animal.hasTrait("carnivore") and animal.population > animal.food:
				return index

		return -1

	""" 
		Gets an attacker and a player + species to attack
		ListOf(Tuple(Nat, Species)), ListOf(PlayerState) -> (Nat, Nat, Nat)
	"""
	@staticmethod
	def getCarnivoreAttack(species, otherPlayers):
		prey = False
		carnIndex = defPlayerIndex = preyIndex = -1
		for i, animal in species:
			if animal.hasTrait("carnivore"):
				canAttack = False
				# get a player with an attackable animal
				for j in range(len(otherPlayers)):
					defender = otherPlayers[j]
					# get an attackable animal; range so that we can check bounds before getting neighbors
					for k in range(len(defender.species)):
						lNeighbor, rNeighbor = defender.getNeighbors(k)
						if (Species.isAttackable(defender.species[k], animal, lNeighbor, rNeighbor) and
																				(defender.species[k].compare(prey)) > 0):
							defPlayerIndex = j
							prey = defender.species[k]
							preyIndex = k
							carnIndex = i
							canAttack = True

				if canAttack:
					return carnIndex, defPlayerIndex, preyIndex
				else:
					return -1, -1, -1

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
			False - no feeding at this time
			Nat - index of Species fed
			[Nat, Nat] - index of fat-tissue Species fed, amount of fatFood
			[Nat, Nat, Nat] - index of carnivore, index of player to attack, index of species to attack
		PlayerState, Nat, ListOf(PlayerState) -> FeedingAction
	"""
	@staticmethod
	def feed(curState, wateringHole, players):
		species = SillyPlayer.indexSpecies(curState)
		myIndex, otherPlayers = SillyPlayer.getIndex(curState, players)

		fatTissueSpecies, currentNeed = SillyPlayer.getFatTissueSpecies(species, wateringHole)
		if fatTissueSpecies is not False:
			return [fatTissueSpecies, currentNeed]

		vegetarian = SillyPlayer.getVegetarian(species)
		if vegetarian is not False:
			return vegetarian

		carnivore, defender, prey = SillyPlayer.getCarnivoreAttack(species, otherPlayers)
		if carnivore is not False:
			if myIndex is not False and defender >= myIndex:
				defender += 1
			return [carnivore, defender, prey]

		# none can be fed
		return False
