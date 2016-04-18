PURPOSE:

Make our Evolution game runnable in a distributed fashion.

FILES:
13/main-client will run regular client players

13/cheat-client1 will run a client player that will randomly cheat during steps 2 and 3

13/cheat-client2 will run a client player that will randomly cheat during step 4

13/main-server will run the server

13/[client|server]/dealer.py is the dealer of the Evolution game

13/server/proxyPlayer.py is an external player proxy

13/client/proxyDealer.py is an external dealer proxy

13/client/cheatChoose.py is the player strategy for cheating in steps 2 and 3

13/client/cheatFeed.py is the player strategy for cheating in step 4

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

Before running, first change HOST_IP and HOST_PORT in main-client and main-server to match your own.
To run the game, first run ./main-server N where N is the number of external players you wish to accept.
Then, run ./main-client to create 1 player; run in multiple windows/on multiple machines to meet the required
number you set in the server. 

You may wish to change the TIMEOUT values in those files to give yourself more time to start up the clients.

If you'd like to try out the cheating players, run cheat-client[1|2] in lieu of a main-client. They will print
a message on every step they attempt to cheat so you can confirm whether or not the server successfully noticed
their shenanigans and kicked them.

To run the unit tests, run python test<FileName>.py


READING THE CODE:

Start by reading the code in dealer.py and playerState.py for a broad overview and context.
Then, read proxyPlayer.py and proxyDealer.py.
Read into subsequent files as needed.
