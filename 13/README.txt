PURPOSE:

Make our Evolution game runnable in a distributed fashion.

FILES:
13/main-server will run the server

13/main-client will run regular client players

13/cheat-client1 will run a client player that will randomly cheat during steps 2 and 3

13/cheat-client2 will run a client player that will randomly cheat during step 4


RUNNING THE CODE:

To run the game, first run ./main-server PORT <OPT: IP>. 
Then, run ./main-client PORT <OPT: IP> to create 1 player; run in multiple windows/on multiple machines.
The game will automatically start after there are at least 3 players and the TIMEOUT has been exceeded.

You may wish to change the TIMEOUT values in main-server and main-client to give yourself more time to start up extra clients.

If you'd like to try out the cheating players, run cheat-client[1|2] in lieu of a main-client. They will print
a message on every step they attempt to cheat so you can confirm whether or not the server successfully noticed
their shenanigans and kicked them. Note that they randomly decide when to cheat, which means that they may not cheat at all.

To run the unit tests, run python test<FileName>.py


READING THE CODE:

Start by reading the code in server/dealer.py and server/playerState.py for a broad overview and context.
Then, read server/proxyPlayer.py and client/proxyDealer.py.
Read into subsequent files as needed.
