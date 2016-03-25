# Representation of the dealer in a game of Evolution
from species import *
from sillyPlayer import *
from drawing import Drawing


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
		Display the essence of a dealer
		Void -> Void
	"""
	def display(self):
		Drawing(dealer=self)

	"""
		Actually feed a species based on its traits and decrement the watering hole as needed
		Fat tissue species should NOT be fed here -- they are fed elsewhere
		@param player: the player who owns the species to be fed
		@param species: the index of the species who's being fed
		@param foodCount: how much food species should be fed 
		PlayerState, Nat, Nat -> Void
	"""
	def feedFromWateringHole(self, curPlayer, specIdx, foodCount=1, fatFood=False):
		spec = curPlayer.species[specIdx]
		amountFed = 0

		if fatFood:
			amountFed = curPlayer.feedFatFood(specIdx, min(foodCount, self.wateringHole))
			self.wateringHole -= amountFed
		else:
			amountFed = curPlayer.feedSpecies(specIdx, foodCount, self.wateringHole)
			self.wateringHole -= amountFed

	"""
		Execute a carnivore attack, including feeding
		@param attPlayer: the player who owns the attacking species
		@param defPlayer: the player who owns the defending species
		@param defend: the species that's being attacked
		@param attIdx: the index of the species that's attacking
		PlayerState, PlayerState, Nat, Nat -> Void 
	"""
	def executeAttack(self, attPlayer, defPlayer, attIdx, defendIdx):
		att = attPlayer.species[attIdx]
		defend = defPlayer.species[defendIdx]

		defend.population -= 1
		self.extinctSpecies(defPlayer, defendIdx)

		if defend.hasTrait("horns"):
			att.population -= 1
			self.extinctSpecies(attPlayer, attIdx)

		if att.population > att.food:
			self.feedFromWateringHole(attPlayer, attIdx, 1)

	"""
		Clear a now-extinct species and give pity cards to the species' owner
		If the species owner's last remaining species dies, remove that player from the players being fed this round
		@param player: the player whose species just went the way of the dodo
		@param speciesIdx: the species to Clear
		PlayerState, Nat -> Void
	"""
	def extinctSpecies(self, player, speciesIdx):
		if player.species[speciesIdx].population <= 0:
			self.distributeCards(player, 2)
			del player.species[speciesIdx]
			if not player.species:
				del self.currentlyFeeding[self.currentlyFeeding.index(player)]

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
			self.currentlyFeeding.remove(player)
			return True
		elif (len(hungry) == 1) and not hungry[0][1].hasTrait("carnivore") and not hungry[0][1].hasTrait("fat-tissue"):
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
	def queryFeed(self, queryPlayer):
		decision = SillyPlayer.feed(queryPlayer, self.wateringHole, self.players)
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
			del self.currentlyFeeding[self.currentlyFeeding.index(queryPlayer)]
			return False

	"""
	Execute automatic feedings triggered by scavenger traits.
	@param player: current PlayerState
	"""
	def scavengeFeed(self, curPlayer):
		for i in range(len(curPlayer.species)):
			spec = curPlayer.species[i]
			if spec.hasTrait("scavenger"):
				self.feedFromWateringHole(curPlayer, i, 1)
		try:
			nextPlayer = self.players[self.players.index(curPlayer)+1]
			self.scavengeFeed(nextPlayer)
		except:
			# There are no more players to be fed after the current player 
			pass


	"""
	Execute the next step in the feeding routine; either feeding the next player automatically
	or querying the player for their feeding decision, and completing subsequent triggered feedings

	#Invariants: wateringHole must be greater than 0
	Void -> Void
	"""
	def feed1(self):
		curPlayer = self.players[0]
		if self.wateringHole > 0:
			if not self.autoFeed(curPlayer):
				attack = self.queryFeed(curPlayer)
				if attack:
					self.scavengeFeed(curPlayer)

	#TODO: iterate through Players and call helper feed1
