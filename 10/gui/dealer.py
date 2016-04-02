# Representation of the dealer in a game of Evolution
from drawing import Drawing
from traitCard import *
from playerState import *


class Dealer:
	wateringHole = 0
	players = []
	currentlyFeeding = []
	deck = []
	discard = []

	"""
		Create a Dealer
		@param playersList: list of all players still in the game
		@param currentlyFeeding: list of all players who are still being fed this turn
		@param wateringHole: the number of food tokens remaining in the watering hole
		@param deck: the cards in the deck that have not yet been dealt to players
		TODO: when do we update playersList AND currentlyFeeding?
	"""
	def __init__(self, playersList, wateringHole, deck):
		self.wateringHole = wateringHole
		self.players = playersList
		self.currentlyFeeding = playersList[:]
		self.deck = deck

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

		except:
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
			player.hand.append(self.deck.pop(0))

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

	#Invariants: wateringHole must be greater than 0
	Void -> Void
	"""
	def feed1(self):
		curPlayer = self.currentlyFeeding[0]
		if not self.autoFeed(curPlayer):
			attack = self.queryFeed(curPlayer)
			if attack:
				self.scavengeFeed(curPlayer)

	#TODO: iterate through Players and call helper feed1
