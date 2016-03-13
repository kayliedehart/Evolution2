# Representation of the dealer in a game of Evolution
import sys
sys.path.append("../feeding")
import species
import player

class Dealer:
	wateringHole = 0
	players = []
	deck = []
	discard = []

	def __init__(self, playersList, wateringHole, deck):
		self.wateringHole = wateringHole
		self.players = playersList
		self.deck = deck

	"""
		Actually feed a species based on its traits and decrement the watering hole as needed
		Fat tissue species should NOT be fed here -- they are fed elsewhere
		@param player: the player who owns the species to be fed
		@param species: the species who's being fed
		@param foodCount: how much food species should be fed 
		PlayerState, Species, Nat -> Void
	"""
	def feedFromWateringHole(self, curPlayer, spec, foodCount):
		if spec.hasTrait("foraging"):
			foodCount += 1
		if (self.wateringHole >= foodCount) and (spec.food + foodCount <= spec.population):
			spec.food += foodCount
			self.wateringHole -= foodCount
		elif (spec.food + foodCount <= spec.population):
			spec.food += self.wateringHole
			self.wateringHole = 0

		left, right = Player.getNeighbors(curPlayer, spec)

		if species.hasTrait("cooperation"):
			self.feedFromWateringHole(curPlayer, right, 1)

	"""
		Execute a carnivore attack, including feeding
		@param attPlayer: the player who owns the attacking species
		@param defend: the species that's being attacked
		@param att: the species that's attacking
		Player, Species, Species -> Void 
		TODO: remove a species if its population drops to 0?
	"""
	def executeAttack(self, attPlayer, defend, att):
		defend.population -= 1
		if defend.hasTrait("horns"):
			att.population -= 1
		if att.population > att.food:
			self.feedFromWateringHole(attPlayer, att, 1)


	"""
		Try to automatically feed a species of the given player. If there is only one remaining
		hungry species, and it's a herbivore, it can be automatically fed.
		Return True on success.
		@param player: the current PlayerState
		Player -> Boolean
	"""
	def autoFeed(self, player):
		hungry = []
		for s in player.species:
			if not (s.population > s.food or (s.body > s.fatFood and s.hasTrait("fat-tissue"))):
				hungry.append(s)

		if (len(hungry) == 1) and not (hungry[0].hasTrait("carnivore")):
			# if the only species is a herbivore but has unfilled fat-tissue, must query
			if hungry[0].hasTrait("fat-tissue") and hungry[0].body > hungry[0].fatFood:
				return False
			else:
				self.feedFromWateringHole(player, hungry[0], 1)
				return True
		return False

	"""
		Query the given player for what species to feed next, and feed according to 
		response. Return whether the query resulted in a successful attack. 
		@param player: the current PlayerState
		@return Boolean: if feeding took place
	"""
	def queryFeed(self, player):
		decision = Player.feed(player, self.wateringHole, self.players)
		if decision:
			if type(decision) == int:
				self.feedFromWateringHole(player, player.species[decision], 1)
				return False
			if len(decision) == 2:
				if self.wateringHole >= decision[1]:
					player.species[decision[0]].fatFood += decision[1]
					self.wateringHole -= decision[1]
				else:
					player.species[decision[0]].fatFood += self.wateringHole
					self.wateringHole = 0
				return False
			if len(decision) == 3:
				attacker = player.species[decision[0]]
				defender = self.players[decision[1]]
				prey = defender.species[decision[2]]
				left, right = Player.getNeighbors(defender, prey)
				if Species.isAttackable(defender, attacker, left, right):
					self.executeAttack(player, defender, attacker)
					return True
		else:
			return False

	"""
	Execute automatic feedings triggered by scavenging traits.
	@param player: current PlayerState
	"""
	def scavengeFeed(self, curPlayer):
		for spec in curPlayer.species:
			if spec.hasTrait("scavenging"):
				self.feedFromWateringHole(curPlayer, spec, 1)
		try:
			nextPlayer = self.players[self.players.index(curPlayer)+1]
			self.scavengeFeed(nextPlayer)
		except:
			# no need to keep going 
			pass


	"""
	Execute the next step in the feeding routine; either feeding the next player automatically
	or querying the player for their feeding decision, and completing subsequent triggered feedings

	#Invariants: wateringHole must be greater than 0
	@param configuration: a list of PlayerStates
	"""
	def feed1(self, configuration):
		curPlayer = configuration[0]
		if wateringHole > 0:
			if not self.autoFeed(curPlayer):
				attack = self.queryFeed(curPlayer)
				if attack:
					self.scavengeFeed(curPlayer)

	#TODO: iterate through Players and call helper feed1
	# remove Players from list if they have no hungry species