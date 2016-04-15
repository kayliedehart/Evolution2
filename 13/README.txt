PURPOSE:

Make our Evolutiong game runnable in a distributed fashion.

FILES:
13/main-client will run client players

13/main-server will run the server

13/[client|server]/dealer.py is the dealer of the Evolution game

13/server/proxyPlayer.py is an external player proxy

13/client/proxyDealer.py is an external dealer proxy

13/[client|server]/playerState.py is the player data representation

13/[client|server]/species.py represents a Species Board

13/[client|server]/traitCard.py represents a TraitCard

13/[client|server]/action4.py represents an Action4

13/[client|server]/replaceTrait.py represents a ReplaceTrait (RT) action

13/[client|server]/buySpeciesBoard.py represents a BuySpeciesBoard (BT) action

13/[client|server]/gainBodySize.py represents a GainBodySize(GB) action

13/[client|server]/gainPopulation.py represents a GainPopulation(GP) action

13/[client|server]/test[fileName].py are the unit tests for the given fileName


RUNNING THE CODE:

To run the game, first run ./main-server N where N is the number of external players you wish to accept.
Then, run ./main-client N. 

To run the unit tests, run python test<FileName>.py


READING THE CODE:

Start by reading the code in dealer.py and playerState.py for a broad overview and context.
Read into subsequent files as needed.