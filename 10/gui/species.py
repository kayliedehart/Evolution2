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
		traits: Traits (String) on this species board (up to 3)
		fatFood: how much food has been stored on a fat tissue card
				 can only be non-zero when a fat tissue card is in self.traits
		Nat, Nat, Nat, ListOf(Trait), Nat -> Species
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
		return name in self.traits

	"""
		comparator for species/OptSpecies (aka False or Species)
		decides if a species is larger than the given; precedence is decided in the following order:
			population size, food eaten, body size
		output is as follows:
			if self is larger than given OR given is False, return is positive
			if self is the same as as given, return is 0
			if self is smaller than given, return is negative
		OptSpecies -> Boolean
	"""
	def compare(self, other):
		if other is False:
			return 1

		if self.population != other.population:
			return self.population - other.population
		elif self.food != other.food:
			return self.food - other.food
		else:
			return self.body - other.body

	"""
		Checks if this species can avoid an attack with warning-call
		@param attack: attacking species
		@param lNeighbor: this species' left neighbor, if one exists
		@param rNeighbor: this species' right neighbor, if one exists
		@return False if attack cannot attack self, True otherwise
	"""
	def checkWarningCall(self, attack, lNeighbor, rNeighbor):
		if (lNeighbor and lNeighbor.hasTrait("warning-call")) or (rNeighbor and rNeighbor.hasTrait("warning-call")):
			return attack.hasTrait("ambush")
		return True

	"""
		Checks if this species meets the conditions for successfully burrowing
		@return False if this species can successfully burrow, True otherwise
	"""
	def checkBurrowing(self):
		return not (self.hasTrait("burrowing") and self.food == self.population)

	"""
		Checks if this species can avoid an attack by climbing
		@param attack: attacking species
		@return False if attack cannot attack self, True otherwise
	"""
	def checkClimbing(self, attack):
		return not (self.hasTrait("climbing") and not attack.hasTrait("climbing"))

	"""
		Checks if this species can avoid an attack with hard shell
		@param attack: attacking species
		@return False if attack cannot attack self, True otherwise
	"""
	def checkHardShell(self, attack):
		attackBody = attack.body
		if attack.hasTrait("pack-hunting"):
			attackBody += attack.population
		return not (self.hasTrait("hard-shell") and not (attackBody - self.body >= 4))

	"""
		Checks if this species can fend off an attack with herding and horns
		@param attack: attacking species
		@return False if attack cannot attack self, True otherwise
	"""
	def checkHerding(self, attack):
		attackPopulation = attack.population
		if self.hasTrait("horns"):
			attackPopulation -= 1
		return not (self.hasTrait("herding") and not (attackPopulation - self.population > 0))

	"""
		Checks if this species has a symbiotic relationship with its right-side neighbor
		@param rNeighbor: this species' right neighbor, if one exists
		@return False if the neighbor does its neighborly duties, True if this species is still open to attack
	"""
	def checkSymbiosis(self, rNeighbor):
		return not (self.hasTrait("symbiosis") and (rNeighbor and (rNeighbor.body > self.body)))

	"""
		Can attack perform an attack against defend, given its two neighbors lNeighbor and rNeighbor?
		@param defend: the defending species
		@param attack: the attacking species
		@param lNeighbor: the defending species' neighbor to the left
		@param rNeighbor: the defending species' neighbor to the right
		@return True if attack can perform an attack against defend, False if it cannot
		Species, Species, OptSpecies, OptSpecies -> Boolean where OptSpecies are one of Species or False
	"""
	@staticmethod
	def isAttackable(defend, attack, lNeighbor, rNeighbor):
		return attack.hasTrait("carnivore") and defend.population > 0 \
											and (defend.checkWarningCall(attack, lNeighbor, rNeighbor)
													and defend.checkBurrowing()
													and defend.checkClimbing(attack)
													and defend.checkHardShell(attack)
													and defend.checkHerding(attack)
													and defend.checkSymbiosis(rNeighbor)) 

