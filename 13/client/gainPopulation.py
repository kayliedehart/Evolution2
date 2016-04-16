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
	Void -> JsonArray
	"""
	def toJson(self):
		return [self.specIdx, self.cardIdx]

	"""
	JSON -> GainPopulation
	"""
	@staticmethod
	def fromJson(GP):
		GainPopulation.validate(GP)
		spec, card = GP
		return GainPopulation(spec, card)


	"""
	Check if a given list of JSON GainPopulations is valid
	EFFECT: If the list is invalid, quit
	JSON -> Void
	"""
	@staticmethod
	def validate(GP):
		spec, card = GP
		if not(len(GP) == 2 and type(spec) == int 
							and type(card) == int):
			quit()

