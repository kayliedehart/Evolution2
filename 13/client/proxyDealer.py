# the internal representation of an external dealer
from playerState import *
import json

TIMEOUT = 1
MAX_JSON_SIZE = 2048

class ProxyDealer:
	self.player = False
	self.sock = False

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
			try:
				message = json.loads(message)
				resp = self.delegateMessage(message)
				if resp:
					self.sock.sendall(json.dumps(resp))
			except Exception e: # find the actual exception when json tries to load an incomplete thing
				print "Unexpected end of message"
				quit()

		print "Game over!"

	"""
		Takes a message from the server, calls the appropriate player method, and prepares its response
		JsonArray -> Opt: JsonArray
	"""
	def delegateMessage(self, message):
		if len(message) == 3:
			if type(message[0]) == int and type(message[1]) == list and type(message[2]) == list: #PlayerState
				self.start(message)
		elif len(message) == 2:
			if type(message[0]) == list and type(message[1]) == list: #[[[Species, Species, ...], [Species, Species, ...]], [[Species, Species, ...], [Species, Species, ...]]]
				return self.choose(message)
		elif len(message) == 5:
			if type(message[0]) == int and type(message[1]) == list and type(message[2]) == list
				and type(message[3]) == int and type(message[4]) == list: # PlayerState, WateringHole, [[Species, Species, ...],[Species, Species, ...]]
				return self.feedNext(message)
		else:
			quit()

	"""
		JsonArray(PlayerState) -> Void
	"""
	def start(self, state):
		self.player.start(PlayerState.playerStateFromJson(state))

	"""
		JsonArray -> JsonArray
	"""
	def choose(self, otherPlayers):
		befores = [[Species.speciesFromJson(spec) for spec in player] for player in otherPlayers[0]]
		afters = [[Species.speciesFromJson(spec) for spec in player] for player in otherPlayers[1]]
		return Action4.toJson(self.player.choose(befores, afters))

	"""
		JsonArray -> JsonArray
	"""
	def feedNext(self, gameState):
		curState = PlayerState.playerStateFromJson(gameState[0], gameState[1], gameState[2])
		otherPlayers = [[PlayerState(0, 0, [Species.speciesFromJson(spec)], []) for spec in player] for player in gameState[4]]
		otherPlayers.append(curState)
		return self.player.feedNext(curState, gameState[3], otherPlayers)
