README

__init__.py - necessary for python to recognize packages
remote-client - runs a remote proxy wrapper for a 6 Nimmt! player

To run remote, try running ./remote-client from a machine with python2.7 in its PATH.
Otherwise, it can be run by invoking it with python 2.7 any other way. 

To read through remote, start at the __init__() function, then read through each 
function as it's called in playGame(). The game first waits for a start-round, 
then takes turns and chooses stacks when asked in the proper order. 
