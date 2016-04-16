# A Player's request to increase a Species' body size

class GainBodySize:

	"""
		Construct a new GainBodySize
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
	def fromJson(GB):
		GainBodySize.validate(GB)
		spec, card = GB
		return GainBodySize(spec, card)

	"""
	Check if a given list of JSON GainBodySizes is valid
	EFFECT: If the list is invalid, quit
	JSON -> Void
	"""
	@staticmethod
	def validate(GB):
		spec, card = GB
		if not(len(GB) == 2 and type(spec) == int 
							and type(card) == int):
			quit()


