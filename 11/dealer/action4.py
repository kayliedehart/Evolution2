# A Representation for an "Action4" in a game of Evolution
from gainPopulation import *
from gainBodySize import *
from buySpeciesBoard import *
from replaceTrait import *

class Action4:

	"""
		Construct a new Action4
		@param cardIdx: the index of the traitCard donated by the Player in their hand
		@param GP: a list of zero or more GainPopulation 
		@param GB: a list of zero or more GainBodySize 
		@param BT: a list of zero or more BuySpeciesBoard 
		@param RT: a list of zero or more ReplaceTrait 
		Nat, [GainPopulation, ...], [GainBodySize, ...], [BuySpeciesBoard, ...], [ReplaceTrait, ...] -> Void
	"""
	def __init__(self, cardIdx, GP, GB, BT, RT):
		self.tribute = cardIdx
		self.GP = GP
		self.GB = GB
		self.RT = RT
		self.BT = BT


	"""
	Construct an Action4 from the given JSON input
	EFFECT: if the input is invalid, quit
	@param action4: JSON representation of an Action4
	@return an Action4 equivalent to the JSON
	JSON -> Action4
	"""
	@staticmethod
	def actionFromJson(action4):
		Action4.validate(action4)
		cardIdx, GP, GB, BT, RT = action4

		return Action4(cardIdx, [GainPopulation.fromJson(p) for p in GP[1:]], 
								[GainBodySize.fromJson(b) for b in GB[1:]], 
								[BuySpeciesBoard.fromJson(buyt) for buyt in BT], 
								[ReplaceTrait.fromJson(rept) for rept in RT])

	"""
		Validate a JSON Action4
		EFFECT: if not valid, quit
		JSON -> Void
	"""
	@staticmethod
	def validate(action4):
		pass
