README

Implement the interface for all components of the 6 Nimmt game other than the player. 

__init__.py - Treats this directory as a package (for linking)
MainProgram.py - Creates the players and kicks off the game
Dealer.py - Manages the turns and round of a 6 Nimmt game
GameBoard.py - Places and removes stacks, awards points
Stack.py - Manages a single stack
Deck.py - Generates and shuffles a deck of cards
Card.py - Create a single card with face value and bull points
Tests.py - Contains unit tests for testable 6 Nimmt functions
Constants.py - Keeps track of global 6 Nimmt constants

If you wish to run tests, you will also need to apply the patch 3/test-config.patch to link the player in.
Do this by running "patch -p1 < 3/starting-config.patch" from the top-level directory (cs4500-kotubyp-maxxb95/). 
Then, run "python MainProgram.py [number of players for the game]" (or any equivalent command that invokes Python 2.7.x) in this directory, where number of players is the integer number of players you'd like to simulate (between 2 and 10).

To understand this program, read the files in the order given above. The main functionality resides in the first three files. The interface to be implemented is given in Player.py. The Stack, Deck, and Card classes will contain basic information about board management and game objects. __init__ can be ignored entirely. 
