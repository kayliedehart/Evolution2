PURPOSE:

Create a GUI to display the current Dealer and a single Player to moniter the progress of a game of Evolution.
Create a test harness to act as a controller between the view components and the underlying game logic.  

FILES:

10/xgui is the test harness for the GUI

10/xgui-[n]-in.json is a json Dealer configuration to be run with xgui

10/gui/dealer.py is the dealer of the Evolution game

10/gui/drawing.py is the view component of the GUI

10/gui/ham.gif is an image resource used in the GUI

10/gui/SillyPlayer.py is a player implementation with the current silly player strategy

10/gui/playerState.py is the player data representation

10/gui/species.py represents a Species Board

10/gui/traitCard.py represents a TraitCard

10/gui/test[fileName].py are the unit tests for the given fileName

RUNNING THE CODE:

To run the test harness, run ./xgui <json-input> 

To run the unit tests, run python test<FileName>.py

READING THE CODE:

Start by reading the code in dealer.py and playerState.py for a broad overview and context.
Read into subsequent files as needed.

