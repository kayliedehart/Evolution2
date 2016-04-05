# Representation of the dealer in a game of Evolution
from drawing import Drawing
from traitCard import *
from playerState import *
from action4 import Action4


class Dealer:
	wateringHole = 0
	players = []
	currentlyFeeding = []
	deck = []
	# indices of cards players have played this turn
	# it contains (index of player, index of card played)
	# used to avoid mutation of lists when using indexes
	cardsPlayed = [] 
	discard = []

	"""
		Create a Dealer
		@param playersList: list of all players still in the game
		@param currentlyFeeding: list of all players who are still being fed this turn
		@param wateringHole: the number of food tokens remaining in the watering hole
		@param deck: the cards in the deck that have not yet been dealt to players
	"""
	def __init__(self, playersList, wateringHole, deck):
		self.wateringHole = wateringHole
		self.players = playersList
		self.currentlyFeeding = playersList[:]
		self.deck = deck
		self.discard = []
		self.cardsPlayed = []

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
		Create a dict from this dealer
		None -> Dict
	"""
	def toDict(self):
		return {"wateringHole": self.wateringHole, 
				"deck": [card.toDict() for card in self.deck], 
				"players": [player.toDict() for player in self.players]}

	"""
		Display the essence of a dealer
		Void -> Void
	"""
	def display(self):
		Drawing(dealer=self.toDict())

	"""
		creates a Dealer from a json array
		JsonArray -> Dealer
	"""
	@staticmethod
	def dealerFromJson(dealer):
		try:
			if type(dealer[0]) == list:
				players = [PlayerState.playerStateFromJson(player) for player in dealer[0]]
			if type(dealer[1]) == int:
				wateringHole = dealer[1]
			if type(dealer[2]) == list:
				cards = [TraitCard.traitCardFromJson(card) for card in dealer[2]]

			return Dealer(players, wateringHole, cards)

		except Exception as e:
			quit()

	"""
		creates a json array describing a given internal Dealer
		Void -> JsonArray
	"""
	def dealerToJson(self):
		return [[PlayerState.playerStateToJson(player) for player in self.players], 
				self.wateringHole,
				[TraitCard.traitCardToJson(card) for card in self.deck]]

	"""
		Remove a player from the currentlyFeeding list
		Done in cases where a player has no more species to feed this turn
			or does not wish to continue feeding this turn
		@param player: the player to remove
		PlayerState -> Void
	"""
	def removePlayerFromTurn(self, player):
		if player in self.currentlyFeeding:
			del self.currentlyFeeding[self.currentlyFeeding.index(player)]
		else:
			raise ValueError("Player is already finished for this turn!")

	"""
		Actually feed a species based on its traits and decrement the watering hole.

		@param player: the player who owns the species to be fed
		@param species: the index of the species who's being fed
		@param foodCount: how much food species should be fed 
		PlayerState, Nat, Nat -> Void
	"""
	def feedFromWateringHole(self, curPlayer, specIdx, foodCount=1, fatFood=False):
		if fatFood:
			amountFed = curPlayer.feedFatFood(specIdx, min(foodCount, self.wateringHole))
			self.wateringHole -= amountFed
		else:
			amountFed = curPlayer.feedSpecies(specIdx, foodCount, self.wateringHole)
			self.wateringHole -= amountFed

	"""
		Execute a carnivore attack: reduce Species populations, check if 
		Species are extinct, and if the attacker is not Extinct, feed.

		@param attPlayer: the player who owns the attacking species
		@param defPlayer: the player who owns the defending species
		@param defIdx: the species that's being attacked
		@param attIdx: the index of the species that's attacking
		PlayerState, PlayerState, Nat, Nat -> Void 
	"""
	def executeAttack(self, attPlayer, defPlayer, attIdx, defIdx):
		defPlayer.executeAttack(defIdx)

		if defPlayer.speciesHasTrait(defIdx, "horns"):
			attPlayer.executeAttack(attIdx)

		isDefExtinct = self.extinctSpecies(defPlayer, defIdx)
		isAttExtinct = self.extinctSpecies(attPlayer, attIdx)

		if not isAttExtinct:
			self.feedFromWateringHole(attPlayer, attIdx, 1)

	"""
		Clear a now-extinct species and give pity cards to the species' owner
		If the species owner's last remaining species dies, remove that player 
		from the players being fed this round.

		@param player: the player whose species just went the way of the dodo
		@param speciesIdx: the species to clear
		@return whether the species was successfully removed
		PlayerState, Nat -> Boolean
	"""
	def extinctSpecies(self, player, speciesIdx):
		isExtinct = player.isExtinct(speciesIdx)
		if isExtinct:
			self.distributeCards(player, 2)
			player.removeSpecies(speciesIdx)
			if player.hasNoSpecies():
				self.removePlayerFromTurn(player)
		
		return isExtinct

	"""
		Distribute cards to a player
		Cards are given from the head of the deck
		@param player: player who is being given cards
		@param numCards: the number of cards to give to the player
		PlayerState, Nat -> Void
	"""
	def distributeCards(self, player, numCards):
		for i in range(min(numCards, len(self.deck))):
			player.addCards([self.deck.pop(0)])

	"""
		Try to automatically feed a species of the given player.
		- If the given player has no species, autofeed will remove it from the list of players
		  being fed this turn
		Otherwise, will automatically feed:
		- a lone hungry herbivore 
		@param player: the current PlayerState
		@return True if a herbivore feeding or player removal occurs.
		PlayerState -> Boolean
	"""
	def autoFeed(self, player):
		hungry = player.getHungrySpecies()

		if len(hungry) == 0:
			self.removePlayerFromTurn(player)
			return True
		elif (len(hungry) == 1) and not player.speciesHasTrait(hungry[0][0], "carnivore") and not player.speciesHasTrait(hungry[0][0], "fat-tissue"):
			self.feedFromWateringHole(player, hungry[0][0], 1)
			return True

		return False

	"""
		Query the given player for what species to feed next, and feed according to 
		response. Return whether the query resulted in a successful attack. 
		@param player: the current PlayerState
		@return Boolean: if a carnivore attack took place
		PlayerState -> Boolean
	"""
	#TODO:  Consider making decision an object, decision.execute()
	def queryFeed(self, queryPlayer):
		decision = queryPlayer.feed(self.wateringHole, self.players)
		if decision is not False:
			if type(decision) == int:
				self.feedFromWateringHole(queryPlayer, decision, 1)
				return False
			if len(decision) == 2:
				self.feedFromWateringHole(queryPlayer, decision[0], foodCount=decision[1], fatFood=True)
				return False
			if len(decision) == 3:
				defender = self.players[decision[1]]
				if queryPlayer.verifyAttack(defender, decision[0], decision[2]):
					self.executeAttack(queryPlayer, defender, decision[0], decision[2])
					return True
		else:
			self.removePlayerFromTurn(queryPlayer)
			return False

	"""
		Execute automatic feedings triggered by scavenger traits.
		@param player: current PlayerState
	"""
	def scavengeFeed(self, curPlayer):
		for player in self.currentlyFeeding:
			self.wateringHole -= player.scavenge(self.wateringHole)

	"""
	Execute the next step in the feeding routine; either feeding the next player automatically
	or querying the player for their feeding decision, and completing subsequent triggered feedings

	ASSUME: wateringHole must be greater than 0
	Void -> Void
	"""
	def feed1(self):
		curPlayer = self.currentlyFeeding[0]
		if not self.autoFeed(curPlayer):
			attack = self.queryFeed(curPlayer)
			if attack:
				self.scavengeFeed(curPlayer)

		if curPlayer in self.currentlyFeeding:
			self.currentlyFeeding = self.currentlyFeeding[1:] + self.currentlyFeeding[:1]


	"""
	For each upgrade request, move the player's payment 
	to the discard list, and modify the requested species field.
	@param playerIdx: index of the current player upgrading
	@param gain: a gainPopulation or gainBodySize list
	@param gfunc: the appropriate player function to call in order to modify
	
	Nat, list of (gainPopulation xor gainBodySize), function -> Void
	"""
	def playerGains(self, playerIdx, gain, gfunc):
		for g in gain:
			self.updateDiscards([(playerIdx, g.cardIdx)])
			gfunc(g.specIdx)

	"""
	Give the PlayerState a new SpeciesBoard with a population of 1 and
	the requested traits, and move all cards to the discard.
	@param player: the index to the PlayerState to be updated
	@param purchase: the buySpeciesBoard requests being carried out
	Nat, list of buySpeciesBoard -> Void
	"""
	def createSpecBoard(self, playerIdx, purchase):
		for p in purchase:
			self.players[playerIdx].addSpecies(p.traitList)

			trashCards = p.traitList[:]
			trashCards.append(p.payment)

			self.updateDiscards([(playerIdx, cardIdx) for cardIdx in trashCards])

	"""
	Update PlayerState per a Player's requests for increases in population, 
	bodysize, or creating additional SpeciesBoards.
	@param playerIdx: the index of the PlayerState to be updated
	@param purchases: the Action4 to be carried out
	Nat, Action4 -> Void
	"""
	def buyUpgrades(self, playerIdx, purchases):
		self.createSpecBoard(playerIdx, purchases.BT)
		self.playerGains(playerIdx, purchases.GP, self.players[playerIdx].addPopulation)
		self.playerGains(playerIdx, purchases.GB, self.players[playerIdx].addBody)

	"""
	Get a list of TraitCard objects from a list of indexes pointing at them
	@param moves: The list of (player's index, index of their card)
	@return a list of TraitCard that those moves represented
	ListOf((Nat, Nat)) -> ListOf(TraitCard)
	"""
	def getPlayerCards(self, moves):
		return [self.players[moves[i][0]].hand[moves[i][1]] for i in range(len(moves))]

	"""
	Update the permanent discard as well as the temporary cards-played to have the most recently-played cards
	@param moves: the PlayerIndex, CardIndex tuples
	@param cards: the actual TraitCards that correspond to the moves
	ListOf((Nat, Nat)) -> Void
	"""
	def updateDiscards(self, moves):
		self.cardsPlayed += moves
		self.discard += self.getPlayerCards(moves)

	"""
	Update the wateringHole with the food value of all donated cards, 
	and then discard cards. 
	@param tributes = list of (player index, card player wants to play)
	ListOf(Nat, Nat) -> Void
	"""
	def replenishWateringHole(self, tributes):
		tributeCards = self.getPlayerCards(tributes)
		self.wateringHole += sum([tribute.food for tribute in tributeCards])
		self.wateringHole = max(0, self.wateringHole)
		self.updateDiscards(tributes)

	"""
	 EFFECT: Adds population to any fertile species, feeds long necks, and moves previously
	 stored fatFood to regular food for each species.
	 Void -> Void
	"""
	def prelimAutoFeedings(self):
		for player in self.players:
			player.fertile()

		for player in self.players:
			self.wateringHole -= player.longNeck(self.wateringHole)

		for player in self.players:
			player.transferFatFood()

	"""
	Update PlayerState per a Player's requests to exchange old traits on
	a species with new ones from their hand.
	@param player: index of the PlayerState to be updated
	@param actions: the Action4 to be carried out; using RT
	Nat, Action4 -> Void
	"""
	def replaceTraits(self, playerIdx, actions):
		for rt in actions.RT:
			self.players[playerIdx].replaceTrait(rt.specIdx, rt.oldTraitIdx, rt.newTraitIdx)
			self.updateDiscards([(playerIdx, rt.newTraitIdx)])

	"""
	Removes any cards players have played from their hands and resets the list of cards played this turn
	Done after buying all upgrades/updating all traits so that indexes within a hand don't change
	Void -> Void
	"""
	def revokePlayedCards(self):
		cardsDict = {}
		for i in range(len(self.players)):
			cardsDict[i] = []

		for playerIdx, cardIdx in self.cardsPlayed:
			cardsDict[playerIdx] += [cardIdx]

		for playerIdx, cardIdcs in cardsDict.items():
			self.players[playerIdx].discardFromHand(cardIdcs)

		self.cardsPlayed = []

	"""
	EFFECT: based on player actions, update PlayerStates, replenish wateringHole, 
	carry out automatic feedings from the wateringHole, and then initialize the
	round-robin feeding cycle. 

	@param actions: list of Action4
	ASSUME:  (length players) == (length card-actions)
		the actions are specified in the same order as players
	List of Action4 -> Void 
	"""
	def step4(self, actions):
		self.replenishWateringHole([(playerIdx, action.tribute) for playerIdx, action in enumerate(actions)])
		for i in range(len(self.players)):
			self.buyUpgrades(i, actions[i])
			self.replaceTraits(i, actions[i])
		self.revokePlayedCards()
		self.prelimAutoFeedings()

		self.currentlyFeeding = self.players[:]	
		while (self.wateringHole > 0) and (len(self.currentlyFeeding) > 0):
			self.feed1()


































