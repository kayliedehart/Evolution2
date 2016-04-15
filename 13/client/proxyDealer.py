# the internal representation of an external dealer
from playerState import *
import json

TIMEOUT = 10
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
			message = self.sock.recv(MAX_JSON_SIZE)
			print "message {}".format(message)
			try:
				message = json.loads(message)
				resp = self.delegateMessage(message)
				if resp:
					self.sock.sendall(json.dumps(resp))
			except Exception as e: # find the actual exception when json tries to load an incomplete thing
				print e
				print message
				print "Unexpected end of message"
				#quit()

		print "Game over!"

	"""
		Takes a message from the server, calls the appropriate player method, and prepares its response
		JsonArray -> Opt: JsonArray
	"""
	def delegateMessage(self, message):
		if len(message) == 3:
			print "3"
			if type(message[0]) == int and type(message[1]) == list and type(message[2]) == list: #PlayerState
				self.start(message)
		elif len(message) == 2:
			print "2"
			if type(message[0]) == list and type(message[1]) == list: #[[[Species, Species, ...], [Species, Species, ...]], [[Species, Species, ...], [Species, Species, ...]]]
				return self.choose(message)
		elif len(message) == 5:
			print "5"
			if type(message[0]) == int and type(message[1]) == list and type(message[2]) == list and type(message[3]) == int and type(message[4]) == list: # PlayerState, WateringHole, [[Species, Species, ...],[Species, Species, ...]]
				return self.feedNext(message)
		else:
			print "bad msg validation in delegate"
			quit()

	"""
		JsonArray(PlayerState) -> Void
	"""
	def start(self, state):
		print "Start"
		self.player.start(self.stateFromJson(state))

	"""
		JsonArray -> JsonArray
	"""
	def choose(self, otherPlayers):
		print "choose"
		befores = [[Species.speciesFromJson(spec) for spec in player] for player in otherPlayers[0]]
		afters = [[Species.speciesFromJson(spec) for spec in player] for player in otherPlayers[1]]
		return Action4.actionToJson(self.player.choose(befores, afters))

	"""
		JsonArray -> JsonArray
	"""
	def feedNext(self, gameState):
		print "feedNext"
		curState = self.stateFromJson(gameState[0], gameState[1], gameState[2])
		otherPlayers = [[PlayerState(0, 0, [Species.speciesFromJson(spec)], []) for spec in player] for player in gameState[4]]
		otherPlayers.append(curState)
		return self.player.feedNext(curState, gameState[3], otherPlayers)

	"""
		JsonArray -> PlayerState
	"""
	def stateFromJson(self, state):
		species = [Species.speciesFromJson(animal) for animal in state[1]]
		cards = [TraitCard.traitCardFromJson(card) for card in state[2]]
		# TODO: this is probably why everything is breaking
		return PlayerState(state[0], 0, species, cards, self)
