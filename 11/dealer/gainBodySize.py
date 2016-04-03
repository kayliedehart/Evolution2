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
	JSON -> GainPopulation
	"""
	@staticmethod
	def fromJson(GB):
		GainBodySize.validate(GB)
		if GB:
			key, spec, card = GB
			return GainBodySize(spec, card)
		else:
			return []


	"""
	Check if a given list of JSON GainBodySizes is valid
	EFFECT: If the list is invalid, quit
	JSON -> Void
	"""
	@staticmethod
	def validate(GP):
		pass

