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
	Void -> JsonArray
	"""
	def toJson(self):
		return [self.specIdx, self.oldTraitIdx, self.newTraitIdx]

	"""
	JSON -> ReplaceTrait
	"""
	@staticmethod
	def fromJson(RT):
		ReplaceTrait.validate(RT)
		specIdx, oldTraitIdx, newTraitIdx = RT
		return ReplaceTrait(specIdx, oldTraitIdx, newTraitIdx)

	"""
	Check if a given list of JSON ReplaceTraits is valid
	EFFECT: If the list is invalid, quit
	JSON -> Void
	"""
	@staticmethod
	def validate(RT):
		specIdx, oldTraitIdx, newTraitIdx = RT
		if not(len(RT) == 3 and type(specIdx) == int 
							and type(oldTraitIdx) == int 
							and type(newTraitIdx) == int):
			quit()
