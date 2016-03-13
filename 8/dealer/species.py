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
