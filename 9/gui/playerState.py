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