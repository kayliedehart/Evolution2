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
	JSON, PlayerState -> GainPopulation
	"""
	@staticmethod
	def fromJson(GB, player):
		GainBodySize.validate(GB, player)
		key, spec, card = GB
		return GainBodySize(spec, card)

	"""
	Check if a given list of JSON GainBodySizes is valid
	EFFECT: If the list is invalid, quit
	JSON, PlayerState -> Void
	"""
	@staticmethod
	def validate(GB, player):
		key, spec, card = GB
		if not(len(GB) == 3 and key == "body" 
							and type(spec) == int 
							and type(card) == int):
			quit()


