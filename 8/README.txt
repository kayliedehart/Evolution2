README - Assignment 7

__init__.py - necessary for this to be considered a package
compile - returns an exit code of 0 (can't pre-compile python)
test_xattack.py - a suite of unit tests for xattack
test_xfeed.py - a suite of unit tests for xfeed
xattack - a proxy for the dealer to access species.isAttackable
xfeed - a proxy for the dealer to access player.feed

To run xfeed, run ./xfeed < input-json > out.
To run xattack, run ./xattack < input-json > out.

To understand xfeed and xattack, you may wish to read the code it calls. 
Follow the README in /feeding to understand that code, then read the 
programs themselves.

NOTE: We worked in the assignment 6 directory for some time before copying
everything over to 7 and continuing work, so a partially-fixed version of 
this code exists in 6/. 
