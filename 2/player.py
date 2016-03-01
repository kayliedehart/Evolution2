'''
###############
### Purpose ###
###############

Describe the Interface of Player components in the 6Nimmt! program.


##################
### Background ###
##################

To provide some context for how the Player component fits into the
implementation of the game, we will briefly describe the flow of the game from
the point of view of the Player implementation.

The program consists of three components: a Dealer, a Player, and a main
program that coordinates the interactions between the Dealer and the Player.
Since we will be developing multiple different Player implementations, the goal
is to keep the role of the Player as simple as possible. Doing so will allow
us to quickly prototype different stratgies and game scenarios. More specifically,
this means that the state of the game will be maintained by the Dealer component
and sent to the Player as needed.

A Player is instantiated via the default Python constructor with a list of Card
objects that represent the Player's hand at the start of the game.

After a Player is instantiated, it will have three responsibilities.
    1. A Player must be able to be dealt new cards via a receive_cards() method.

    2. A Player must be able to pick a card to discard via the discard_card() method.
        -- The Player will receive the state of the game when this method is called.

    3. A Player must be able to pick a Stack (via the pick_stack() method) whose
    bull points will be added to their bull point total.
        -- This is called when the face value of the card that the Player
        discarded is less than the face value of the top card of all of the stacks.
        -- The Player will receive the state of the game when this method is called.

All of these methods will be called at the appropriate times, which means
the Player does not need to track the state of the game. The Player is only
responsible for the tracking the cards it holds in its hand.


########################
### Data Definitions ###
########################

    -- A Card is a collections.namedtuple('Card', ['face_value', 'bull_number'])
        -- Card.face_value is an integer that is between 1 and 104 inclusive.
        -- Card.bull_number is an integer that is between 2 and 7 inclusive.
        -- Each Card represents one of the cards in the 6Nimmt! deck.

    -- A PlayerID is a non-negative integer.
        -- Each Player in the game has a unique PlayerID

    -- A PlayerScore is a non-negative integer.
        -- The PlayerScore represents the number of bull points a Player has lost.

    -- A Stack is a list of Cards, ordered from bottom to top
        -- Each Stack represents one of the 4 stacks of cards where a card
        can be placed.

    -- A GameState is a dictionary with the following key, value pairs.
        -- All keys in the dictionary are strings.
        -- Key -> Value
            -- 'player_scores' -> Dictionary of {PlayerID: PlayerScore}
            -- 'stacks' -> List of Stacks.
                -- Each Stack represents a location where a card can be placed.
            -- 'cards_played' -> Set of Cards that have been played in the game.
                -- This includes all cards that are in a Stack or have been discarded.


########################
### Player Interface ###
########################

The Player interface must implement the following constructor and 3 public
methods:
'''

class Player:
    cards = None

    def __init__(self, cards):
        """Instantiate the Player with his cards.

        args:
            cards: List of Cards that are dealt to the Player
        return: None

        example:
            ExamplePlayer([Card(2, 3), Card(54, 7), Card(23, 5)...])
        """

        self.cards = cards

    def receive_cards(self, cards):
        """Adds the given cards to the the player's hand.

        args:
            cards: List of Cards that are given to the Player
        return: None

        example:
            p.receive_cards([Card(2, 3), Card(54, 7), Card(23, 5)...])
        """

        self.cards.extend(cards)

    def discard_card(self, game_state):
        """Choose 1 card from hand to be discarded.

        args:
            game_state: The GameState that helps determine which card to discard

        return: A Card that the Player possesses.

        example:
            p.discard_card({
                        'stacks': [
                                    [Card(1, 7), ]
                                    [Card(44, 6), ]
                                    [Card(25, 3), ]
                                    [Card(67, 2), ]
                                  ]
                        'player_scores': {
                                            0: 24
                                            1: 17
                                         }
                        'cards_played': set([
                                                Card(1, 7),
                                                Card(44, 6),
                                                Card(25, 3),
                                                Card (67, 2),
                                            ])
                    }) -> Card(23, 3)
        """
        self.cards.sort(key=lambda tup: tup[0])
        bestCard = self.cards[len(self.cards) - 1]
        del self.cards[-1]
        return bestCard

    def pick_stack(self, game_state):
        """Choose the stack whose bull points will be added to the Player's total.

        args:
            game_state: The GameState used to pick which Stack to choose

        return: An int that represents the list index of the chosen stack
        in game_state['stacks']

        In the example below, returning 2 would pick the stack [Card(25, 3), ]

        example:
            p.pick_stack({
                        'stacks': [
                                    [Card(89, 7), ]
                                    [Card(44, 6), ]
                                    [Card(25, 3), ]
                                    [Card(67, 2), ]
                                  ]
                        'player_scores': {
                                            0: 24
                                            1: 17
                                         }
                        'cards_played': set([
                                                Card(89, 7),
                                                Card(44, 6),
                                                Card(25, 3),
                                                Card (67, 2),
                                            ])
                    }) -> 2

        When implementing, we chose to ignore the above example, since it
        chose the stack with the lowest face_value sum and not the lowest
        bull_points sum. Below is another example we added:

        p.pick_stack({
                        'stacks': [
                                    [Card(89, 7), Card(50, 5), Card(34, 2)]
                                    [Card(44, 6), Card(35, 7)]
                                    [Card(25, 3), Card(43, 5)]
                                    [Card(67, 2), Card(89, 1), Card(43, 3)]
                                  ]
                        'player_scores': {
                                            0: 24
                                            1: 17
                                         }
                        'cards_played': set([
                                                Card(89, 7),
                                                Card(44, 6),
                                                Card(25, 3),
                                                Card (67, 2),
                                            ])
                    }) -> 3
        """
        best_stack_index = 0
        lowest_stack_bull_points = float('inf')

        for i in range(len(game_state['stacks'])):
            current_sum = sum(card.bull_points for card in game_state['stacks'][i])
            if current_sum < lowest_stack_bull_points:
                best_stack_index = i
                lowest_stack_bull_points = current_sum

        return best_stack_index
