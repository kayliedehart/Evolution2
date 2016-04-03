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
	JSON -> ReplaceTrait or EmptyList
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
		pass
