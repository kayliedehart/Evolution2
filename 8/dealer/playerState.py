from species import *


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