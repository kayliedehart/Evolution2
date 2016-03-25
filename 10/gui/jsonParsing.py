from traitCard import TraitCard
from species import Species
from playerState import PlayerState
from dealer import Dealer

"""
	All methods in this class process to and from arrays that can be dumped/loaded in json
	However, actual calls to json.dump/load should be made in proxy classes, as they are
	not done here
"""
class JsonParsing:

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


	############ FOR SPECIES

	"""
		creates a json array fitting the spec from the given species
		Species -> JsonArray
	"""
	@staticmethod
	def speciesToJson(species):	
		if species is False:
			return False
		result = [["food", species.food],
				  ["body", species.body],
				  ["population", species.population],
				  ["traits", species.traits]]

		if species.fatFood > 0:
			result.append(["fat-food", species.fatFood])

		return result

	""" 
	   Helper to convert json species to internal Species
	   JSONSpecies = [["food",Nat],
	   ["body",Nat],
	   ["population",Nat],
	   ["traits",LOT],
	   OPT: ["fat-food",Nat]]
	   JSONSpecies -> OptSpecies
	   TODO: make this like playerState where it errors out
	"""
	@staticmethod
	def speciesFromJson(jsonSpecies):    
		# If the if statement errors out, the input is ill shaped
		try:
			if jsonSpecies is False:
				return False

			if jsonSpecies[0][0] == "food" and jsonSpecies[1][0] == "body" and jsonSpecies[2][0] == "population" and jsonSpecies[3][0] == "traits":
				food = jsonSpecies[0][1]
				body = jsonSpecies[1][1]
				population = jsonSpecies[2][1]
				traits = []
				hasFatTissue = False

				for trait in jsonSpecies[3][1] :
					if JsonParsing.checkTrait(trait):
						traits.append(trait)
					if trait == "fat-tissue":
						hasFatTissue = True

				if len(jsonSpecies) == 5 and hasFatTissue and jsonSpecies[4][0] == "fat-food":
					fatFood = jsonSpecies[4][1]
				else:
					fatFood = 0

				return Species(food, body, population, traits, fatFood)
			else:
				pass
				# TODO: what should actually happen when the labels for an array are wrong?

		except Exception as e:
			raise e

	""" 
	   convert a json species from spec to a list of species/optspecies
	   JsonSituation -> [Species, Species, OptSpecies, OptSpecies]
	"""
	@staticmethod
	def situationFromJson(situation):    
		defend = JsonParsing.speciesFromJson(situation[0])
		attack = JsonParsing.speciesFromJson(situation[1])

		if not attack or not defend:
			quit()

		lNeighbor = JsonParsing.speciesFromJson(situation[2]) or Species(0, 0, 0, [], 0)
		rNeighbor = JsonParsing.speciesFromJson(situation[3]) or Species(0, 0, 0, [], 0)

		return defend, attack, lNeighbor, rNeighbor



	########### FOR PLAYERSTATE

	""" 
	   creates a json array of a PlayerState object
	   PlayerState -> JsonArray
	"""
	@staticmethod
	def playerStateToJson(state):
		species = []
		for animal in state.species:
			species.append(JsonParsing.speciesToJson(animal))

		cards = []
		for card in state.hand:
			cards.append(JsonParsing.traitCardToJson(card))

		result = [["id", state.num],
				  ["species", species],
				  ["bag", state.foodbag]]

		if cards:
			result.append(["cards", cards])

		return result

	"""
	   creates a PlayerState from a json array
	   JsonArray -> PlayerState
	   TODO: make this not quite so awful
	   for one: what should happen in the else cases?
	"""
	@staticmethod
	def playerStateFromJson(state):
		id = 0
		bag = -1
		speciesList = []
		cards = []

		try:
			if state[0][0] == "id":
				id = state[0][1]

			if state[1][0] == "species":
				for species in state[1][1]:
					speciesList.append(JsonParsing.speciesFromJson(species))

			if state[2][0] == "bag":
				bag = state[2][1]

			if len(state) == 4 and state[3][0] == "cards":
				for card in state[3][1]:
					cards.append(JsonParsing.traitCardFromJson(card))

			if id > 0 and bag >= 0:
				return PlayerState(id, bag, speciesList, cards)

		except Exception as e:
			raise e


	########## FOR TRAIT CARDS

	"""
		creates a trait card from a json array
		JsonArray -> TraitCard
	"""
	@staticmethod
	def traitCardFromJson(card):
		return TraitCard(card[1], card[0])

	""" 
		creates a json array representing an internal TraitCard
		TraitCard -> JsonArray
	"""
	@staticmethod
	def traitCardToJson(card):
		return [card.food, card.name]


	########## FOR DEALER

	"""
		creates a Dealer from a json array
		JsonArray -> Dealer
	"""
	@staticmethod
	def dealerFromJson(dealer):
		players = []
		wateringHole = -1
		cards = []

		try:
			for player in dealer[0]:
				players.append(JsonParsing.playerStateFromJson(player))

			wateringHole = dealer[1]

			for card in dealer[2]:
				cards.append(JsonParsing.traitCardFromJson(card))

			return Dealer(players, wateringHole, cards)

		except Exception as e:
			raise e

	"""
		creates a json array describing a given internal Dealer
		Dealer -> JsonArray
	"""
	@staticmethod
	def dealerToJson(dealer):
		return [[JsonParsing.playerStateToJson(player) for player in dealer.players], 
				dealer.wateringHole,
				[JsonParsing.traitCardToJson(card) for card in dealer.deck]]

	########## MISCELLANY

	"""
		checks if a given trait name is valid
		String -> Boolean
	"""
	@staticmethod
	def checkTrait(trait):
		return trait in JsonParsing.allTraits


