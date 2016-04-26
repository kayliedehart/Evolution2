# the internal representation of an external dealer
from playerState import *
from species import *
from action4 import *
from traitCard import *
import json
import time
import socket

TIMEOUT = 30
MAX_JSON_SIZE = 2048

class ProxyDealer:
	player = False
	sock = False

	"""
		Player, Socket -> ProxyDealer
	"""
	def __init__(self, player, socket):
		self.player = player
		self.sock = socket
		self.sock.settimeout(TIMEOUT)
		self.main()

	"""
		Listen for commands/updates from the server, delegate to local player as needed
	"""
	def main(self):
		message = "ok"
		while message != "":
			time.sleep(.01)
			message = self.sock.recv(MAX_JSON_SIZE)
			try:
				ourResp = json.loads(message)
				resp = self.delegateMessage(ourResp)
				if resp is not "" and resp is not None:
					self.sock.sendall(json.dumps(resp))
			except (socket.timeout, socket.error, ValueError) as e:
				self.sock.close()
				#print e
				#print "Unexpected end of message"
				quit()

		print "Game over!"

	"""
		Takes a message from the server, calls the appropriate player method, and prepares its response
		JsonArray -> Opt: JsonArray
	"""
	def delegateMessage(self, message):
		if len(message) == 4:
			if type(message[0]) == int and type(message[1]) == int and type(message[2]) == list and type(message[3]) == list: 
				self.start(message)
		elif len(message) == 2:
			if type(message[0]) == list and type(message[1]) == list: 
				return self.choose(message)
		elif len(message) == 5:
			if type(message[0]) == int and type(message[1]) == list and type(message[2]) == list and type(message[3]) == int and type(message[4]) == list: 
				return self.feedNext(message)
		else:
			print "bad msg validation in delegate"
			quit()

	"""
		@param state: a wateringhole and playerstate
		(throw away the watering hole because we're bad at this game)
		JsonArray(PlayerState) -> Void
	"""
	def start(self, state):
		self.player.start(self.stateFromJson(state[1:]))

	"""
		JsonArray -> JsonArray
	"""
	def choose(self, otherPlayers):
		befores = [[Species.speciesFromJson(spec) for spec in player] for player in otherPlayers[0]]
		afters = [[Species.speciesFromJson(spec) for spec in player] for player in otherPlayers[1]]
		choice = self.player.choose(befores, afters)
		act = Action4.actionToJson(choice)
		return act

	"""
		JsonArray -> JsonArray
	"""
	def feedNext(self, gameState):
		curState = self.stateFromJson(gameState[0:3])
		otherPlayers = []
		for player in gameState[4]: 
			otherPlayers.append(PlayerState(0, 0, [Species.speciesFromJson(spec) for spec in player], []))
		otherPlayers.append(curState)
		return self.player.feed(curState, gameState[3], otherPlayers)

	"""
		JsonArray -> PlayerState
	"""
	def stateFromJson(self, state):
		species = [Species.speciesFromJson(animal) for animal in state[1]]
		cards = [TraitCard.traitCardFromJson(card) for card in state[2]]
		return PlayerState(state[0], 0, species, cards, self)
