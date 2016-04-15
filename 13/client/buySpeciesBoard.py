# A Player's request to buy a new Species Board with Trait Cards

class BuySpeciesBoard:

	"""
		Construct a BuySpeciesBoard
		Nat, List of Nat -> Void
	"""
	def __init__(self, paymentIdx, traitIdces):
		self.payment = paymentIdx
		self.traitList = traitIdces

	"""
	Void -> JsonArray
	"""
	def toJson(self):
		result = [self.payment]
		for trait in self.traitList:
			result.append(trait)
		return result

	"""
	JSON, PlayerState -> BuySpeciesBoard
	"""
	@staticmethod
	def fromJson(BT):
		BuySpeciesBoard.validate(BT)
		traitIdcs = [item for item in BT[1:]]
		return BuySpeciesBoard(BT[0], traitIdcs)

	"""
	Check if a given list of JSON BuySpeciesBoard is valid
	EFFECT: If the list is invalid, quit
	JSON -> Void
	"""
	@staticmethod
	def validate(BT):
		for item in BT:
			if not (type(item) == int):
				quit()
