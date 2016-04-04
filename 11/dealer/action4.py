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
		self.BT = BT
		self.RT = RT


	"""
	Construct an Action4 from the given JSON input
	EFFECT: if the input is invalid, quit
	@param action4: JSON representation of an Action4
	@param player: PlayerState that this action corresponds 
	@return an Action4 equivalent to the JSON
	JSON, PlayerState -> Action4
	"""
	@staticmethod
	def actionFromJson(action4, player):
		Action4.validate(action4, player)
		cardIdx, GP, GB, BT, RT = action4

		return Action4(cardIdx, [GainPopulation.fromJson(p, player) for p in GP], 
								[GainBodySize.fromJson(b, player) for b in GB], 
								[BuySpeciesBoard.fromJson(buyt, player) for buyt in BT], 
								[ReplaceTrait.fromJson(rept, player) for rept in RT])

	"""
		Validate a JSON Action4
		EFFECT: if not valid, quit
		@param action4: JSON representation of an Action4
		@param player: PlayerState that this action corresponds 
		JSON, PlayerState -> Void
	"""
	@staticmethod
	def validate(action4, player):
		cardIdx, GP, GB, BT, RT = action4
		if not (len(action4) == 5 and type(cardIdx) == int):
			quit()
		else:
			[GainPopulation.validate(p, player) for p in GP]
			[GainBodySize.validate(b, player) for b in GB]
			[BuySpeciesBoard.validate(buyt, player) for buyt in BT]
			[ReplaceTrait.validate(rept, player) for rept in RT]
