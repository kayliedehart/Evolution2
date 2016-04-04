PURPOSE:

Create a dealer to display the current Dealer and a single Player to moniter the progress of a game of Evolution.
Create a test harness to act as a controller between the view components and the underlying game logic.  

FILES:

11/xstep4 is the test harness for the step4 method in dealer

11/xstep4-[n]-[in|out].json is a [json Dealer configuration, [Actions]] in/expected output pair to be run with xstep4

11/dealer/dealer.py is the dealer of the Evolution game

11/dealer/drawing.py is the view component of the dealer

11/dealer/ham.gif is an image resource used in the dealer

11/dealer/SillyPlayer.py is a player implementation with the current silly player strategy

11/dealer/playerState.py is the player data representation

11/dealer/species.py represents a Species Board

11/dealer/traitCard.py represents a TraitCard

11/dealer/action4.py represents an Action4

11/dealer/replaceTrait.py represents a ReplaceTrait (RT) action

11/dealer/buySpeciesBoard.py represents a BuySpeciesBoard (BT) action

11/dealer/gainBodySize.py represents a GainBodySize(GB) action

11/dealer/gainPopulation.py represents a GainPopulation(GP) action

11/dealer/test[fileName].py are the unit tests for the given fileName

11/api/api.txt is the specification for an interaction API for the Evolution game


RUNNING THE CODE:

To run the test harness, run ./xstep4 < <json-input> 

To run the unit tests, run python test<FileName>.py


READING THE CODE:

Start by reading the code in dealer.py and playerState.py for a broad overview and context.
Read into subsequent files as needed.

