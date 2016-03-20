# Representation of the dealer in a game of Evolution
from species import *
from player import *

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
		Actually feed a species based on its traits and decrement the watering hole as needed
		Fat tissue species should NOT be fed here -- they are fed elsewhere
		@param player: the player who owns the species to be fed
		@param species: the index of the species who's being fed
		@param foodCount: how much food species should be fed 
		PlayerState, Species, Nat -> Void
	"""
	def feedFromWateringHole(self, curPlayer, specIdx, foodCount=1, fatFood=False):
		spec = curPlayer.species[specIdx]
		if fatFood is False:
			if (self.wateringHole >= foodCount) and (spec.food + foodCount <= spec.population):
				spec.food += foodCount
				self.wateringHole -= foodCount
			elif (spec.food + foodCount <= spec.population):
				spec.food += self.wateringHole
				self.wateringHole = 0
		else:
			if (self.wateringHole >= foodCount) and (spec.fatFood + foodCount <= spec.body):
				spec.fatFood += foodCount
				self.wateringHole -= foodCount
			elif (spec.fatFood + foodCount <= spec.body):
				spec.fatFood += self.wateringHole
				self.wateringHole = 0

		if spec.hasTrait("foraging") and self.wateringHole > 0:
			spec.food += 1
			self.wateringHole -= 1 

		left, right = Player.getNeighbors(curPlayer, specIdx)

		if right is not False and spec.hasTrait("cooperation"):
			self.feedFromWateringHole(curPlayer, right, 1)

	"""
		Execute a carnivore attack, including feeding
		@param attPlayer: the player who owns the attacking species
		@param defPlayer: the player who owns the defending species
		@param defend: the species that's being attacked
		@param attIdx: the index of the species that's attacking
		Player, Player, Species, Species -> Void 
	"""
	def executeAttack(self, attPlayer, defPlayer, attIdx, defendIdx):
		att = attPlayer.species[attIdx]
		defend = defPlayer.species[defendIdx]

		if defend.hasTrait("horns"):
			att.population -= 1

		defend.population -= 1

		if defend.population <= 0:
			del defPlayer.species[defPlayer.species.index(defend)]
			handoutIdx = 2
			if len(self.deck) < 2:
				handoutIdx = len(self.deck)
				
			for i in range(handoutIdx):
				defPlayer.hand.append(self.deck[i])
				
			self.deck = self.deck[handoutIdx:]
			#if not defPlayer.species:
			#	del self.currentlyFeeding[self.currentlyFeeding.index(defPlayer)]

		if att.population > att.food:
			self.feedFromWateringHole(attPlayer, attIdx, 1)

	"""
		Try to automatically feed a species of the given player. If there is only one remaining
		hungry species, and it's a herbivore, it can be automatically fed.
		Return True on success.
		@param player: the current PlayerState
		Player -> Boolean
	"""
	def autoFeed(self, player):
		hungry = []
		for i in range(len(player.species)):
			s = player.species[i]
			if s.population > s.food or (s.body > s.fatFood and s.hasTrait("fat-tissue")):
				hungry.append((i, s))

		if (len(hungry) == 1):
			hungrySpec = player.species[hungry[0][0]]
			if not (hungrySpec.hasTrait("carnivore")):
				# if the only species is a herbivore but has unfilled fat-tissue, must query
				if hungrySpec.hasTrait("fat-tissue") and hungrySpec.body > hungrySpec.fatFood:
					return False
				else:
					self.feedFromWateringHole(player, hungry[0][0], 1)
					return True
		return False

	"""
		Query the given player for what species to feed next, and feed according to 
		response. Return whether the query resulted in a successful attack. 
		@param player: the current PlayerState
		@return Boolean: if a carnivore attack took place
	"""
	def queryFeed(self, player):
		decision = Player.feed(player, self.wateringHole, self.players)
		if decision is not False:
			if type(decision) == int:
				self.feedFromWateringHole(player, decision, 1)
				return False
			if len(decision) == 2:
				self.feedFromWateringHole(player, decision[0], foodCount=decision[1], fatFood=True)
				return False
			if len(decision) == 3:
				attacker = player.species[decision[0]]
				defender = self.players[decision[1]]
				prey = defender.species[decision[2]]
				leftIdx, rightIdx = Player.getNeighbors(defender, decision[2])
				left = defender.species[leftIdx]
				right = defender.species[rightIdx]
				if Species.isAttackable(prey, attacker, left, right):
					self.executeAttack(player, defender, decision[0], decision[2])
					return True
		else:
			#del self.currentlyFeeding[self.currentlyFeeding.index(player)]
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
	@param configuration: a list of PlayerStates
	"""
	def feed1(self, configuration):
		curPlayer = configuration[0]
		if self.wateringHole > 0:
			if not self.autoFeed(curPlayer):
				attack = self.queryFeed(curPlayer)
				if attack:
					self.scavengeFeed(curPlayer)

	#TODO: iterate through Players and call helper feed1
	# remove Players from list if they have no hungry species
