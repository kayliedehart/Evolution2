# A Player's request to increase a Species' population

class GainPopulation:

	"""
		Construct a new GainPopulation
		Nat, Nat -> Void
	"""
	def __init__(self, specIdx, cardIdx):
		self.specIdx = specIdx
		self.cardIdx = cardIdx

	"""
	JSON, PlayerState -> GainPopulation
	"""
	@staticmethod
	def fromJson(GP, player):
		GainPopulation.validate(GP, player)
		key, spec, card = GP
		return GainPopulation(spec, card)


	"""
	Check if a given list of JSON GainPopulations is valid
	EFFECT: If the list is invalid, quit
	JSON, PlayerState -> Void
	"""
	@staticmethod
	def validate(GP, player):
		key, spec, card = GP
		if not(len(GP) == 3 and key == "population" 
							and type(spec) == int 
							and type(card) == int):
			quit()

