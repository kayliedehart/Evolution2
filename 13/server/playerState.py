# An internal Player in a game of Evolution
from species import *
from drawing import Drawing 
from sillyPlayer import SillyPlayer
from traitCard import *
from action4 import *
import constants

class PlayerState:
	num = 0
	foodbag = 0
	species = []
	hand = []
	info = ""

	""" 
		Internal representation of a json player
		@param num: Nat+ representing this player's unique ID number
		@param foodbag: Nat representing this player's foodbag
		@param species: A List of this player's Species boards
		@param hand: A List of TraitCards in this player's hand (not on boards/haven't been traded in)
		@param player: the external player with strategic functionality
		@param info: the info that the external player sends over
		Nat, Nat, ListOf(Species), ListOf(TraitCard), ProxyPlayer, String -> PlayerState
	"""
	def __init__(self, id, bag, speciesList, cards, player=None, info=""):
		self.num = id
		self.foodbag = bag
		self.species = speciesList
		self.hand = cards
		self.player = player or SillyPlayer()
		self.info = info


	##### COMMUNICATION WITH EXTERNAL PLAYER

	"""
		start a game (step 1) -- if given a new species, add it, and inform external player of current state
		@param spec: an OptSpecies (given if this player didn't already have a species; otherwise False)
		@param wateringHole: current state of the watering hole in the dealer
		OptSpecies, Nat -> Void
	"""
	def start(self, spec, wateringHole):
		if spec is not False:
			self.species.append(spec)
		self.player.start(self, wateringHole)

	"""
		Choose actions for watering hole tributes and trading and check for cheating
		assumption: list of players is ordered such that players before this one in the list
					play before us, and those after this one in the list play after us
		@param allPlayers: the states of all players currently in the game
		@return an Action4 from the external player or, if that move was cheating, False
		ListOf(PlayerState) -> Action4 or False
	"""
	def choose(self, allPlayers):
		for i in range(len(allPlayers)):
			if allPlayers[i] is self:
				splitIdx = i
		befores = [play.species for play in allPlayers[:splitIdx]]
		afters = [play.species for play in allPlayers[splitIdx+1:]]

		return self.checkCheatAction(self.player.choose(befores, afters))

	"""
		Proxy to call the feed method in the external player
		@param wateringHole: the amount of food that can be eaten
		@param players: all the players in this round
		@return FeedingAction -One of:
			False - no feeding at this time
			Nat - index of Species fed
			[Nat, Nat] - index of fat-tissue Species fed, amount of fatFood
			[Nat, Nat, Nat] - index of carnivore, index of player to attack, index of species to attack
		Nat, ListOf(PlayerState) -> FeedingAction
	"""
	def feed(self, wateringHole, players):
		return self.checkFeedCheat(self.player.feed(self, wateringHole, players))


	##### COMMUNICATION WITH INTERNAL DEALER / RELATED HELPERS

	"""
		Do post-turn cleanup:
		- square up species' populations with what they ate
		- remove starving species
		- move food from species boards to player foodbags
		@return the number of species we removed for being extinct (so that dealer can give us cards)
		Void -> Nat
	"""
	def endOfTurn(self):
		numExtinct = 0
		speciesToRemove = []
		for specIdx in range(len(self.species)):
			self.foodbag += self.species[specIdx].cullStarving()
			if self.isExtinct(specIdx):
				speciesToRemove.append(specIdx)
				numExtinct += 1

		self.species = [self.species[i] for i in range(len(self.species)) if i not in speciesToRemove]
		return numExtinct

	"""
		Get this player's score -- a combo of their foodbag, total population 
		for all species, and total trait cards placed on species
		@return the player's score based on the above
		Void -> Nat
	"""
	def getScore(self):
		score = self.foodbag
		for spec in self.species:
			score += spec.population
			score += len(spec.traits)
		
		return score

	"""
		Number of cards this player needs dealt at the beginning of a turn
		Based on their number of species
		If they have no species, then they should ask for 1 card, as they'll be receiving a new species
		at the beginning of the round
		@return num cards needed
		Void -> Nat
	"""
	def numCardsNeeded(self):
		return 3 + max(1, len(self.species))

	"""
		Feed the given species the given amount of fat food that it requested
		@param specIdx: index of the species to feed
		@param foodCount: amount of food to try to feed
		@return the amount of food this species was given
		Nat, Nat -> Nat
	"""
	def feedFatFood(self, specIdx, foodCount):
		spec = self.species[specIdx]
		if spec.hasTrait("fat-tissue"):
			foodCount = min(foodCount, spec.body - spec.fatFood)
			spec.eatFatFood(foodCount)
			return foodCount
		else:
			raise ValueError("Tried to feed fat food to a species without fat tissue")

	"""
		Feed a given species the amount of food that it requested
		@param specIdx: index of the species to feed
		@param foodCount: amount of food to try to feed
		@param wateringHole: the amount of food in the dealer's watering hole
		@return the total amount of food eaten during this feeding
		Nat, Nat, Nat -> Nat
	"""
	def feedSpecies(self, specIdx, foodCount, wateringHole):
		spec = self.species[specIdx]
		foodCount = min(wateringHole, foodCount, spec.population - spec.food)
		spec.eatFood(foodCount)
		wateringHole -= foodCount

		forageAmount = self.forage(specIdx, wateringHole)
		wateringHole -= forageAmount
		foodCount += forageAmount
		
		foodCount += self.cooperate(specIdx, foodCount, wateringHole)

		return foodCount

	"""
		Transfer fat food that a species stored last turn to its actual food 
		Void -> Void
	"""
	def transferFatFood(self):
		fatTissue = self.getSpeciesWithTrait("fat-tissue")
		for ft in fatTissue:
			self.species[ft].transferFatFood()

	"""
		Replace a TraitCard on the given species
		@param specIdx: the index of the species whose traits need switched out
		@param oldTraitIdx: the index of the old trait card
		@param newTraitIdx: the index of the trait card replacing the old one
		Nat, Nat, Nat -> Void
	"""
	def replaceTrait(self, specIdx, oldTraitIdx, newTraitIdx):
		self.species[specIdx].replaceTrait(oldTraitIdx, self.hand[newTraitIdx])


	##### TRAIT-SPECIFIC FEED METHODS
	# TODO: ABSTRACT EVERYTHING.
	"""
		Give all fertile species this player owns one population
		Void -> Void
	"""
	def fertile(self):
		fertile = self.getSpeciesWithTrait("fertile")
		for spec in fertile:
			self.species[spec].addPopulation()

	"""
		Give all long-necked species this player owns one food, as long as the watering hole
		is large enough to feed them
		@param wateringHole: the dealer's watering hole
		@return the amount of food eaten by the longnecks
		Nat -> Nat
	"""
	def longNeck(self, wateringHole):
		longNeck = self.getSpeciesWithTrait("long-neck")
		return self.getAmountFed(longNeck, 1, wateringHole)

	"""
		If the given species has the foraging trait, give it one more food
		@param specIdx: index of the species to feed
		@param wateringHole: the amount of food in the dealer's watering hole
		@return the amount of food this species ate
	"""
	def forage(self, specIdx, wateringHole):
		spec = self.species[specIdx]
		amountFed = 0
		if wateringHole > 0 and spec.hasTrait("foraging") and spec.population > spec.food:
			spec.eatFood(1)
			amountFed += 1
		return amountFed

	"""
		Cooperate
		@param specIdx: index of the species to feed
		@param foodCount: amount of food to try to feed
		@param wateringHole: the amount of food in the dealer's watering hole
		@return the amount of food all species in the cooperation chain ate
		Nat, Nat, Nat -> Nat
	"""
	def cooperate(self, specIdx, foodCount, wateringHole):
		amountFed = 0
		spec = self.species[specIdx]
		left, right = self.getNeighbors(specIdx)
		if spec.hasTrait("cooperation") and right is not False:
			for i in range(foodCount):
				amountFed += self.getAmountFed([specIdx+1], 1, wateringHole)
		return amountFed

	"""
		After a carnivore attack, have all species with the scavenge trait eat from left to right
		@param wateringHole: the amount of food that can be handed out amongst the scavengers
		@return the amount of food eaten amongst our scavengers
		Nat -> Nat
	"""
	def scavenge(self, wateringHole):
		scavengers = self.getSpeciesWithTrait("scavenger")
		return self.getAmountFed(scavengers, 1, wateringHole)

	"""
		Feeds all species in the given list and returns how much food was eaten overall
		@param specs: a list of the species to feed (indexes)
		@param foodCount: how much to feed each species
		@param wateringHole: how much food can be fed overall
		@return the amount of food fed overall
		ListOf(Nat), Nat, Nat -> Nat
	"""
	def getAmountFed(self, specs, foodCount, wateringHole):
		amountFed = 0
		for specIdx in specs:
			if wateringHole > 0:
				fedThisSpecies = self.feedSpecies(specIdx, foodCount, wateringHole)
				amountFed += fedThisSpecies
				wateringHole -= fedThisSpecies
		return amountFed


	##### VALIDATION

	"""
		Check if an action from our external player would be a cheating move
		Following conditions must pass:
			- All card indexes acted on must exist in our hand and be unique 
			- The highest species index referenced should exist after addition of new species boards
			- Should only be able to replace trait cards that already exist (ie no adding of new trait cards)
		@param action: the action the external player wishes to take
		@return the action or, if it was cheating, False
		Action4 -> Action4 or False
	"""
	def checkCheatAction(self, action):
		if action is not False and (self.checkLegalCards(action.getAllCardIdcs()) 
							   and self.checkLegalSpecies(action.getAllSpecIdcs(), len(action.BT))
							   and self.checkTraitReplacement(action.RT, action.BT)
							   and self.checkTraitAddition(action.BT)
							   and self.checkAdditiveActions(action.GP, Species.canGrowPopulation)
							   and self.checkAdditiveActions(action.GB, Species.canGrowBody)):
			return action
		else:
			return False

	"""
		Check that traits being added to a new species board include no duplicates
		@param BTs: the BuySpeciesBoard objects to check
		@return whether the BTs are legal
		ListOf(BuySpeciesBoard) -> Boolean
	"""
	def checkTraitAddition(self, BTs):
		for bt in BTs:
			for newCardIdx in bt.traitList:
				if self.hand[newCardIdx].name == [self.hand[i].name for i in bt.traitList if i != newCardIdx]:
					return False

		return True

	"""
		Checks that a feed action from the external player is legal
		@param feedAct: the feed action given, which SHOULD be one of:
			[Nat, Nat] - index of fat-tissue Species fed, amount of fatFood
			Nat - index of an herbivore Species fed
			[Nat, Nat, Nat] - index of carnivore, index of player to attack, index of species to attack
			False - no feeding at this time
		@return the feedAct if it's legal, KICK_ME if it is not
	"""
	def checkFeedCheat(self, feedAct):
		if type(feedAct) == list: 
			legalSpec = self.checkLegalSpecies([feedAct[0]])
			if ((len(feedAct) == 2 and self.speciesHasTrait(feedAct[0], "fat-tissue") and self.species[feedAct[0]].canAddFat()) or \
			   																		len(feedAct) == 3) and legalSpec:
				return feedAct
			else:
				return constants.KICK_ME
		elif (type(feedAct) == int and self.checkLegalSpecies([feedAct]) and self.species[feedAct].canEat() and not self.speciesHasTrait(feedAct, "carnivore")) or \
																						  		feedAct is False:
			return feedAct
		else:
			return constants.KICK_ME

	"""
		Check whether GrowPopulations and GrowBodySizes can succeed
		@param GPs: the GrowPopulations to check
		@param GBs: the GrowBodySizes to check
		@return True if these actions can occur, False otherwise
	"""
	def checkAdditiveActions(self, gain, gfunc):
		for g in gain:
			if g.specIdx < len(self.species) and not self.species[g.specIdx].gfunc():
				return False
		return True

	"""
		Check that all species indexes passed correspond to species that
		the player will own by the end of the action
		Used to check for cheating 
		@param specIdcs: indexes of the species the external player asked to modify
		@param numBT: the number of BuyTrait actions being requested
		@return True if moves are legal, False otherwise
		ListOf(Nat) -> Boolean
	"""
	def checkLegalSpecies(self, specIdcs, numBT=0):
		return not ((max(specIdcs) > (numBT + len(self.species) - 1)) or (min(specIdcs) < 0))

	"""
		Check that trait replacement uses legal cards and tries to replace existing traits
		Used to check for cheating in Action4
		@param RTs: the ReplaceTrait actions to check
		@param BTs: the BuySpeciesBoards
		@return True if moves are legal, False otherwise
		ListOf(ReplaceTrait) -> Boolean
	"""
	def checkTraitReplacement(self, RTs, BTs):
		for rt in RTs:
			if (rt.oldTraitIdx < 0) or (rt.specIdx  > (len(self.species) + len(BTs) - 1)):
				return False

			traitLen = False
			if rt.specIdx < len(self.species):
				traitLen = len(self.species[rt.specIdx].traits)
				if self.speciesHasDuplicateTraits(rt):
					return False
			elif rt.specIdx < (len(self.species) + len(BTs)):
				traitLen = len(BTs[rt.specIdx - len(self.species) - 1].traitList)

			if traitLen is False or rt.oldTraitIdx >= traitLen:
				return False

		return True 

	"""
		Tell whether a trait that a player is trying to ReplaceTrait on a species is already on that species
		Only checked for species who already exist; checkTraitAddition() handles this for BuySpeciesBoards
		@param rt: the ReplaceTrait to check
		ReplaceTrait -> Boolean
	"""
	def speciesHasDuplicateTraits(self, rt):
		return self.hand[rt.newTraitIdx].name in [self.species[rt.specIdx].traits[i].name for i in range(len(self.species[rt.specIdx].traits)) if i != rt.oldTraitIdx]

	"""
		Check that the card indexes passed all correspond to cards we own
		and that each index is unique
		Used to check for cheating in an Action4
		@param cardIdcs: the indexes of the cards the external player asked to use
		@return True if the moves are legal, False otherwise
		ListOf(Nat) -> Boolean
	"""
	def checkLegalCards(self, cardIdcs):
		if len(cardIdcs) != len(set(cardIdcs)): # no duplicates
			return False
		if (max(cardIdcs) > (len(self.hand) - 1)) or min(cardIdcs) < 0: # only use cards we have
			return False
		return True

	"""
		Verify that this player can use their own chosen species to attack the other given species
		@param defPlayer: PlayerState of the defending player
		@param defIdx: index of the defending species
		@param attIdx: index of the attacking species: should be one of our own
		PlayerState, Nat, Nat -> Boolean
	"""
	def verifyAttack(self, defPlayer, attIdx, defIdx):
		left, right = defPlayer.getNeighbors(defIdx)
		return Species.isAttackable(defPlayer.species[defIdx], self.species[attIdx], left, right)



	##### GENERAL-PURPOSE/DEMETER'S LAW HELPERS

	"""
		Filter out all fed species to get a list of species that can be fed
		@return a list of (Species' index, Species) for hungry species this player has
		Void -> ListOf((Nat, Species))
	"""
	def getHungrySpecies(self):
		hungry = []
		for i in range(len(self.species)):
			if self.species[i].isHungry():
				hungry.append((i, self.species[i]))

		return hungry

	"""
		Gets the indexes of the species neighboring the given species
		@param speciesIdx: index of the species to get neighbors for
		Nat -> [OptSpecies, OptSpecies] where an OptSpecies is Species or False
	"""
	def getNeighbors(self, speciesIdx):
		if speciesIdx > 0:
			lNeighbor = self.species[speciesIdx - 1]
		else:
			lNeighbor = False

		if speciesIdx < len(self.species) - 1:
			rNeighbor = self.species[speciesIdx + 1]
		else:
			rNeighbor = False

		return [lNeighbor, rNeighbor]

	"""
		Get all species this player owns that has the given trait 
		@param trait: the name of the trait to be checked
		String -> ListOf(SpecIdx)
	"""
	def getSpeciesWithTrait(self, trait):
		return [i for i in range(len(self.species)) if self.speciesHasTrait(i, trait)]

	"""
		EFFECT: Drop the population of the given species as in a carnivore attack
		If the species' food > its population, drop the food as well
		@param specIdx: the index of the species to have its population decremented
		Nat -> Void
	"""
	def executeAttack(self, specIdx):
		self.species[specIdx].executeAttack()

	"""
		Tell whether or not the given species is extinct (i.e. that its population <= 0)
		@param specIdx: index of the species to check
		Nat -> Boolean
	"""
	def isExtinct(self, specIdx):
		return self.species[specIdx].isExtinct()

	"""
		Tell whether the species at the given index has the given trait
		@param specIdx: the index of the species to check
		@param traitName: the name of the trait to check for
		Nat, String -> Boolean
	"""
	def speciesHasTrait(self, specIdx, traitName):
		return self.species[specIdx].hasTrait(traitName)

	"""
		Add one population to a species at the given index
		@param specIdx: index of the species to modify
		Nat -> Void
	"""
	def addPopulation(self, specIdx):
		self.species[specIdx].addPopulation()

	"""
		Add one body size to a species at the given index
		@param specIdx: index of the species to modify
		Nat -> Void
	"""
	def addBody(self, specIdx):
		self.species[specIdx].addBody()

	"""
		Give this player a new species with the given traits
		@param traitIdcs: indices of the trait cards this new species will have, up to 3
		ListOf(Nat) -> Void
	"""
	def addSpecies(self, traitIdcs):
		self.species.append(Species(0, 0, 1, [self.hand[i] for i in traitIdcs], 0))

	"""
		Remove the given species from this player's list of species
		@param specIdx: index of the species to remove
		Nat -> Void
	"""
	def removeSpecies(self, specIdx):
		del self.species[specIdx]

	"""
		Tell whether or not this player has any species
		Void -> Boolean
	"""
	def hasNoSpecies(self):
		return not (len(self.species) > 0)

	"""
		Deletes the cards at the given indices from this player's hand
		@param cardIdcs: the indexes of the cards to remove
		ListOf(Nat) -> Void
	"""
	def discardFromHand(self, cardIdcs):
		self.hand = [self.hand[i] for i in range(len(self.hand)) if i not in cardIdcs]

	"""
		Adds the given TraitCards to the end of this player's hand
		@param cards: the cards to add
		ListOf(TraitCard) -> Void 

	"""
	def addCards(self, cards):
		self.hand = cards + self.hand


	###### EQUALITY, PARSING, PRINTING, AND DISPLAYING
	
	""" 
		override equality
		Any -> Boolean
	"""
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
		else:
			return False

	""" 
		override inequality
		Any -> Boolean
	"""
	def __ne__(self, other):
		return not self.__eq__(other)

	"""
		create dictionary 
		None -> Dict
	"""
	def toDict(self):
		return {"num": self.num, 
				"species": [species.toDict() for species in self.species], 
				"hand": [card.toDict() for card in self.hand], 
				"foodbag": self.foodbag}

	"""
		Display the essence of a player
		Void -> Void
	"""
	def display(self):
		Drawing(player=self.toDict())

	""" 
	   creates a json array of a PlayerState object
	   OLD: used for compatibility with old unit tests, but stateToJson follows current spec
	   Void -> JsonArray
	"""
	def playerStateToJson(self):
		species = [Species.speciesToJson(animal) for animal in self.species]
		cards = [TraitCard.traitCardToJson(card) for card in self.hand]

		result = [["id", self.num],
				  ["species", species],
				  ["bag", self.foodbag]]

		if cards:
			result.append(["cards", cards])

		return result

	""" 
	   creates a json array of a PlayerState object
	   Void -> JsonArray
	"""
	def stateToJson(self):
		species = [Species.speciesToJson(animal) for animal in self.species]
		cards = [TraitCard.traitCardToJson(card) for card in self.hand]

		result = [self.num, species, cards]

		return result

	"""
	   creates a PlayerState from a json array
	   JsonArray -> PlayerState
	"""
	@staticmethod
	def playerStateFromJson(state):
		try:
			cards = []
			if state[0][0] == "id":
				num = state[0][1]
			if state[1][0] == "species":
				speciesList = [Species.speciesFromJson(species) for species in state[1][1]]
			if state[2][0] == "bag":
				bag = state[2][1]
			if len(state) == 4 and state[3][0] == "cards":
				cards = [TraitCard.traitCardFromJson(card) for card in state[3][1]]
			if num > 0 and bag >= 0:
				return PlayerState(num, bag, speciesList, cards)

		except Exception as e:
			print state
			raise e
			#quit()