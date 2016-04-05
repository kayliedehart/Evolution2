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
	JSON, PlayerState -> BuySpeciesBoard
	"""
	@staticmethod
	def fromJson(BT, player):
		BuySpeciesBoard.validate(BT, player)
		traitIdcs = [item for item in BT[1:]]
		return BuySpeciesBoard(BT[0], traitIdcs)

	"""
	Check if a given list of JSON BuySpeciesBoard is valid
	EFFECT: If the list is invalid, quit
	JSON -> Void
	"""
	@staticmethod
	def validate(BT, player):
		for item in BT:
			if not (type(item) == int):
				quit()
