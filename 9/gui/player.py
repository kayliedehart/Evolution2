from species import *


class Player:

	"""
		Sorts a list of species from largest to smallest, giving precedence to population, then food eaten, then body size
		The first Nat in the tuple is the original index the species was at when given by the dealer
		set removeFed to True if you would like to filter out all species that cannot be fed
		listOf(Tuple(Nat, Species)), Opt: Boolean -> listOf(Tuple(Nat, Species))
	"""
	@staticmethod
	def sortSpecies(species, removeFed=False):
		result = species
		if removeFed:
			temp = []
			for i, s in species:
				if s.population > s.food or (s.body > s.fatFood and s.hasTrait("fat-tissue")):
					temp.append((i, s))
			result = temp
			
		result = sorted(result, key=lambda x: (x[1].population, x[1].food, x[1].body), reverse=True)
		return result

	"""
		Gets a fat tissue species with the greatest need and its current needs
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
		Gets the neighbors of the given species index
		PlayerState, Nat -> [OptSpecies, OptSpecies]
	"""
	@staticmethod
	def getNeighbors(player, speciesIdx):
		if speciesIdx > 0:
			lNeighbor = player.species[speciesIdx-1]
		else:
			lNeighbor = False

		if speciesIdx < len(player.species) - 1:
			rNeighbor = player.species[speciesIdx+1]
		else:
			rNeighbor = False

		return [lNeighbor, rNeighbor]

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
						lNeighbor, rNeighbor = Player.getNeighbors(defender, k)
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
		Choose a species to feed
		handed states of all players so strategic moves can be made based on neighbors
		it will return a FeedingAction; see the FeedingAction class for more information
		PlayerState, Nat, ListOf(PlayerState) -> FeedingAction
	"""
	@staticmethod
	def feed(curState, wateringHole, players):
		speciesWithIndices = []
		otherPlayers = []
		myIndex = -1

		# ensure that we are not in other players
		for i in range(len(players)):
			if players[i].num != curState.num:
				otherPlayers.append(players[i])
			else:
				myIndex = i

		for i in range(len(curState.species)):
			speciesWithIndices.append((i, curState.species[i]))
		species = Player.sortSpecies(speciesWithIndices, removeFed=True)

		if not species or wateringHole == 0:
			return False

		fatTissueSpecies, currentNeed = Player.getFatTissueSpecies(species, wateringHole)
		if fatTissueSpecies != -1:
			return [fatTissueSpecies, currentNeed]

		vegetarian = Player.getVegetarian(species)
		if vegetarian != -1:
			return vegetarian

		carnivore, defender, prey = Player.getCarnivoreAttack(species, otherPlayers)
		if (carnivore, defender, prey) != (-1, -1, -1):
			if defender >= myIndex and myIndex > -1:
				defender += 1
			return [carnivore, defender, prey]

		# none can be fed
		return False
