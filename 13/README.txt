PURPOSE:

Create a program that can run a multiplayer game of Evolution.
Implement an API for "external" players. 
Develop test harnesses for these.
Specify a new remote-communication interaction protocol.

FILES:

12/xsilly is the test harness for the step4 method in dealer

12/xsilly-[n]-[in|out].json is a [Player, [LoS], [LoS]], [Action4] in/expected 
							output pair to be run with xsilly

12/dealer/dealer.py is the dealer of the Evolution game

12/dealer/drawing.py is the view component of the dealer

12/dealer/ham.gif is an image resource used in the dealer

12/dealer/SillyPlayer.py is a player implementation with the current silly player strategy

12/dealer/playerState.py is the player data representation

12/dealer/species.py represents a Species Board

12/dealer/traitCard.py represents a TraitCard

12/dealer/action4.py represents an Action4

12/dealer/replaceTrait.py represents a ReplaceTrait (RT) action

12/dealer/buySpeciesBoard.py represents a BuySpeciesBoard (BT) action

12/dealer/gainBodySize.py represents a GainBodySize(GB) action

12/dealer/gainPopulation.py represents a GainPopulation(GP) action

12/dealer/test[fileName].py are the unit tests for the given fileName

12/remote/remote.txt is the specification for a remote interaction API for the Evolution game


RUNNING THE CODE:

To run main, run ./main

To run the test harness, run ./xsilly < <json-input> 

To run the unit tests, run python test<FileName>.py


READING THE CODE:

Start by reading the code in dealer.py and playerState.py for a broad overview and context.
Read into subsequent files as needed.

The code for task 2 is in dealer.py as runGame() and all methods referenced within
    its methods and submethods.
	
The code for task 3 is in sillyPlayer.py, residing in the function choose(). 

