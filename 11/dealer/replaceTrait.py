# A Player's request to replace a Trait on a Species Board

class ReplaceTrait:

	"""
		Construct a new ReplaceTrait
		@param specIdx: index of SpeciesBoard to modify
		@param oldTraitIdx: index of TraitCard on SpeciesBoard to be replaced
		@param newTraitIdx: index of new TraitCard in Player's Hand
		Nat, Nat, Nat -> Void
	"""
	def __init__(self, specIdx, oldTraitIdx, newTraitIdx):
		self.specIdx = specIdx
		self.oldTraitIdx = oldTraitIdx
		self.newTraitIdx = newTraitIdx


	"""
	JSON, PlayerState -> ReplaceTrait
	"""
	@staticmethod
	def fromJson(RT, player):
		ReplaceTrait.validate(RT, player)
		specIdx, oldTraitIdx, newTraitIdx = RT
		return ReplaceTrait(specIdx, oldTraitIdx, newTraitIdx)

	"""
	Check if a given list of JSON ReplaceTraits is valid
	EFFECT: If the list is invalid, quit
	JSON, PlayerState -> Void
	"""
	@staticmethod
	def validate(RT, player):
		specIdx, oldTraitIdx, newTraitIdx = RT
		if not(len(RT) == 3 and type(specIdx) == int 
							and type(oldTraitIdx) == int 
							and type(newTraitIdx) == int):
			quit()
