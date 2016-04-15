# An external Player strategy implementation
from species import *
from action4 import Action4
from playerState import PlayerState
import json
from buySpeciesBoard import BuySpeciesBoard
from replaceTrait import ReplaceTrait
from gainPopulation import GainPopulation
from gainBodySize import GainBodySize

TIMEOUT = 10
MAX_JSON_SIZE = 2048

class ProxyPlayer:
	# Current PlayerState that corresponds to this player
	# Supplied in start()
	state = False
	sock = False


	def __init__(self, socket):
		self.state = False
		self.sock = socket
		self.sock.settimeout(TIMEOUT)

	"""
		Get our own state at the end of step 1 of a game (new species/cards added)
		SillyPlayer does nothing with this
		@param curState: PlayerState representing us
		PlayerState -> Void
	"""
	def start(self, curState):
		print "start"
		self.state = curState
		self.sock.sendall(json.dumps(PlayerState.playerStateToJson(self.state)))

	"""
		Choose an action for steps 2 and 3 of the game
		SillyPlayer just picks the biggest cards in order
		@param befores: all the species of players who went before this one
		@param afters: all the species of players who go before this one
		@return the card to place at the watering hole and what trades to make
		ListOf(ListOf(Species)), ListOf(ListOf(Species)) -> Action4
	"""
	def choose(self, befores, afters):
		print "choose"
		befores = [[Species.speciesToJson(spec) for spec in player] for player in befores]
		afters = [[Species.speciesToJson(spec) for spec in player] for player in afters]
		self.sock.sendall(json.dumps([befores, afters]))
		resp = self.sock.recv(MAX_JSON_SIZE)
		if resp:
			return Action4.actionFromJson(json.loads(resp)) # validate me
		else:
			return False
		
	"""
		Choose a species to feed
		@param curState: current public state of this player
		@param wateringHole: amount of food in wateringHole
		@param players: current public states of all players
		@return FeedingAction -One of:
			[Nat, Nat] - index of fat-tissue Species fed, amount of fatFood
			Nat - index of an herbivore Species fed
			[Nat, Nat, Nat] - index of carnivore, index of player to attack, index of species to attack
			False - no feeding at this time
		PlayerState, Nat, ListOf(PlayerState) -> FeedingAction
	"""
	def feed(self, curState, wateringHole, players):
		print "Feed"
		jsonState = PlayerState.playerStateToJson(curState)
		jsonState.append(wateringHole)
		jsonState.append([[Species.speciesToJson(spec) for spec in player.species] for player in players]) #
		# factor out all that vvvvvv
		self.sock.sendall(json.dumps(jsonState))
		resp = self.sock.recv(MAX_JSON_SIZE)
		if resp:
			return json.loads(resp) # validate me
		else:
			return False # actually throw me out if i took too long
