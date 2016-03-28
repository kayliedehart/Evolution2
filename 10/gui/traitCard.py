class TraitCard():
	"""
		enumerate all possible trait names
		used for checking validity of json trait cards
	"""
	allTraits = [
					"carnivore",
					"warning-call",
					"ambush",
					"burrowing",
					"climbing",
					"hard-shell",
					"pack-hunting",
					"horns",
					"herding",
					"symbiosis",
					"fat-tissue",
					"foraging",
					"cooperation",
					"scavenger",
					"fertile",
					"long-neck"
		    ]

	# create a new trait card
	# String, Opt: Nat -> TraitCard
	def __init__(self, name, food):
		self.name = name
		self.food = food or 0

	# check if two trait cards are equal
	# Any -> Boolean
	def __eq__(self, that):
		if isinstance(that, TraitCard):
			return self.name == that.name and self.food == that.food
		else:
			return False

	"""
		Create a dict from this trait card
		None -> Dict
	"""	
	def toDict(self):
		return {"name": self.name,
				"food": self.food}

	"""
		creates a trait card from a json array
		JsonArray -> TraitCard
	"""
	@staticmethod
	def traitCardFromJson(card):
		return TraitCard(card[1], card[0])

	""" 
		creates a json array representing an internal TraitCard
		Void -> JsonArray
	"""
	def traitCardToJson(self):
		return [self.food, self.name]

	"""
		checks if a given trait name is valid
		String -> Boolean
	"""
	@staticmethod
	def checkTrait(trait):
		return trait in TraitCard.allTraits