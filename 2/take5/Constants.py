"""
Constants for the 6 Nimmt! game
"""

NUM_PLAYERS = 4
PLAYER_ORDER = "ASC"
NUM_CARDS = 104
# 104 bullpoints. Index 0 will be assigned to card 1, etc.
# If the list is too short, Deck will generate randomly from that point on
"""
an example list of bullpoints
BULL_POINTS = [6, 5, 7, 4, 4, 3, 2, 4, 2, 2, 5, 2, 7, 4, 5, 7, 3, 4, 4, 3, 7, 2, 5, 4, 7, 6, 4, 6, 5, 7, 5, 4, 5, 3, 4,
                3, 7, 2, 4, 5, 6, 7, 2, 5, 5, 3, 2, 4, 3, 2, 2, 3, 4, 2, 7, 4, 3, 5, 2, 7, 4, 7, 6, 5, 6, 4, 4, 6, 2, 5,
                4, 2, 6, 7, 4, 6, 7, 6, 6, 4, 4, 6, 4, 7, 3, 7, 2, 4, 6, 7, 5, 7, 2, 7, 4, 3, 5, 6, 5, 7, 5, 2, 4, 6]
"""
BULL_POINTS = []
DEFAULT_PLAYER_NUM = 0
MIN_FACE_VALUE = 1
MAX_FACE_VALUE = 104
MIN_BULLPOINTS = 2
MAX_BULLPOINTS = 7
CARDS_PER_PLAYER = 10
NUM_STACKS = 4