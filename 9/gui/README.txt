PURPOSE:

Create a GUI to display the current Dealer and a single Player to moniter the progress of a game of Evolution.
Create a test harness to act as a controller between the view components and the underlying game logic.  

FILES:

9/xgui is the test harness for the GUI

9/xgui-[n]-in.json is a json Dealer configuration to be run with xgui

9/gui/dealer.py is the dealer of the Evolution game

9/gui/drawing.py is the view component of the GUI

9/gui/ham.gif is an image resource used in the GUI

9/gui/jsonParsing.py handles parsing from a JSON configuration to Evolution game objects

9/gui/player.py is a player implementation with the current silly player strategy

9/gui/playerState.py is the player data representation

9/gui/species.py represents a Species Board

9/gui/traitCard.py represents a TraitCard

9/gui/test[fileName].py are the unit tests for the given fileName

RUNNING THE CODE:

To run the test harness, run ./xgui <json-input>

NOTE: In order to see the Player configuration, you must first close the Dealer GUI window. The windows are opened in series. It was assumed that in an actual game, the dealer and players would be running in separate instances, and only one view would be needed at a time; implementations that opened the windows simultaneuously did so at the expense of good OOD principles, so were ultimately discarded. 

READING THE CODE:

Start by reading the code in dealer.py and playerState.py for a broad overview and context, and then read the code in drawing.py to understand the view representation. Read into subsequent files as needed. 

