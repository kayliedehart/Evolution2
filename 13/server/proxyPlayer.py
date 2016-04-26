# An external Player strategy implementation
from species import *
from action4 import Action4
from playerState import PlayerState
import json
import time
import socket
from buySpeciesBoard import BuySpeciesBoard
from replaceTrait import ReplaceTrait
from gainPopulation import GainPopulation
from gainBodySize import GainBodySize
import constants

TIMEOUT = 30
MAX_JSON_SIZE = 2048

class ProxyPlayer:
	# Current PlayerState that corresponds to this player
	# Supplied in start()
	state = False
	sock = False


	"""
		Constructor for a proxy player
		Takes in a socket that is its connection to the client
		EFFECT: the socket also has its timeout set
	"""
	def __init__(self, socket):
		self.state = False
		self.sock = socket
		self.sock.settimeout(TIMEOUT)

	"""
		Get our own state at the end of step 1 of a game (new species/cards added)
		SillyPlayer does nothing with this
		@param curState: PlayerState representing us
		@param wateringHole: the current state of the watering hole in dealer
		PlayerState, Nat -> Void
	"""
	def start(self, curState, wateringHole):
		self.state = curState
		gameState = [wateringHole]
		gameState += PlayerState.stateToJson(self.state)
		self.sock.sendall(json.dumps(gameState))

	"""
		Gets the response for a query from the client
		@return the response or, if the socket timed out, the "kick me out" value
		Void -> JsonValue or KICK_ME
	"""
	def getResponse(self):
		time.sleep(.01) # avoid connection reset by peer problem
		try:
			resp = json.loads(self.sock.recv(MAX_JSON_SIZE))
		except (socket.timeout, ValueError, socket.error): # timeout or invalid json
			resp = constants.KICK_ME
		return resp

	"""
		Choose an action for steps 2 and 3 of the game
		SillyPlayer just picks the biggest cards in order
		@param befores: all the species of players who went before this one
		@param afters: all the species of players who go before this one
		@return the card to place at the watering hole and what trades to make
		ListOf(ListOf(Species)), ListOf(ListOf(Species)) -> Action4
	"""
	def choose(self, befores, afters):
		befores = [[Species.speciesToJson(spec) for spec in player] for player in befores]
		afters = [[Species.speciesToJson(spec) for spec in player] for player in afters]
		time.sleep(.01)
		self.sock.sendall(json.dumps([befores, afters]))
		resp = self.getResponse()
		if resp != constants.KICK_ME:
			return Action4.actionFromJson(resp)
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
		jsonState = PlayerState.stateToJson(curState)
		jsonState.append(wateringHole)
		jsonState.append([[Species.speciesToJson(spec) for spec in player.species] for player in players])
		time.sleep(.01) 
		self.sock.sendall(json.dumps(jsonState))
		return self.getResponse()

