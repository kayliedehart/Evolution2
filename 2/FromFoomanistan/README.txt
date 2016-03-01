Project 2
The purpose of this project is to implement the provided
interface in our programming language and implement the rest
of the system for the game 6 Nimmt!

-----------------------------------------------------------------
player.py
This file is the implementation of the player interface that
was provided.
	- Ambiguities: 
		- In our provided interface, it appears that we were 
		provided with much more than is necessary, including 
		function specifications for the main program, dealer 
		class, gameboard class, stack class, card class, and 
		deck class. To create the player interface, we used 
		only what was provided for the functions needed for 
		the player.
		- One change we made to the provided interface, was 
		with the choose_card function, we decided that the 
		input for a 'board' was unneccessary, so we removed it.

main.py
This file is a wrapper script that runs the 6 Nimmt! game.


dealer.py
This file contains the main logic for the entire game, deciding
the steps and logic that the rules of the game must follow, 
dealing cards out to players, and handling the board.


board.py
This file contains the information for the board class, 
which holds the four stacks for the game.

deck.py
This file contains the information for the deck class, 
which holds the list of cards.

card.py
This file contains the information about a card, which contains
a face value and a bull point value.

unit_tests.py
This file contains all the unit tests for all of the files.

AIPlayer.py
This file uses the player interface to create a computer-player
to run the simulation.

-----------------------------------------------------------------
How to Use the Program
To run the program:
	- cd into the take5 directory.
	- run 'python main.py <players>' where <players> is the
	desired number of players to simulate

The final results of the game will be printed out to the console,
showing the order in which people won.

-----------------------------------------------------------------
Road Map
To read and fully understand the code it is best to follow the 
following order.

card.py -> In this file you can understand the structure of a 
card and the rules between its possible values. The Card is used 
throughout the simulation.

deck.py -> In this file you can understand the different ways we 
can initialize a deck made up of Cards. Read the init function 
and its cases.

board.py -> You can start by understanding it's structure. The 
representation of the stacks is an important place to start. The 
logic on how a specific stack gets updated is also in this file. 
The different functions all help down the road with the dealer.

player.py -> This is important to read through to understand what 
is expected from a player in the rest of our code.

AIPlayer.py -> This is the player we created for the simulation. 
Reading through how it chooses a card is the only difference 
from player.py.

dealer.py -> This is where most of the simulation takes place. 
Understanding all the prior files is important to fully 
understand this file. Its best to first read through the init 
function to understand what a Dealer contains. After that, you
should read through each function before the play_game function.
It will be helpful when reading through play_game to understand
what all the helper functions inside of it do.

unit_tests.py -> This is where all the testing for each file is 
done. After understanding all of the previous code it will be 
easier to read through this by knowing what the functions we 
are testing are doing.

main.py -> Read through to understand how the game initiates 
and outputs the simulation.


