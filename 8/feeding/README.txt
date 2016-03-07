README - Assignment 7

__init__.py - makes this folder into a Python package
constants.py - a container for constant values in evolution
diagram.txt - a top-level UML diagram of our classes
player.py - a player of evolution, including the feed method
playerState.py - information necessary to a player (split to prevent cheating)
species.py - representation of an evolution species
tests.py - Internal unit tests for these classes
traitCard.py - a trait card with a name and food value

To use species.py, you'll want to use xattack in the containing folder. 
See that README for how to run it.
To use player.py, you'll want to use xfeed the same way.
To run tests, run python2.7 tests.py from command line.

To understand the code, we recommend you read through in the following order:
- diagram.txt
- playerState.py
- traitCard.py (since it's very short)
- species.py, the init and isAttackable functions
- player.py, especially the feed function
- tests.py
