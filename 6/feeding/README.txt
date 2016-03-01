README - Assignment 6

__init__.py - makes this folder into a Python package
constants.py - a container for constant values in evolution
feedingAction.py - any action that can be taken during feeding
player.py - a player of evolution, including the feed method
playerState.py - information necessary to a player (split to prevent cheating)
species.py - representation of an evolution species
tests.py - Internal unit tests for these classes

To use species.py, you'll want to use xattack in the containing folder. 
See that README for how to run it.
To use player.py, you'll want to use xfeed the same way.
To run tests, run python2.7 tests.py from command line. NOTE: This will state
that there are only 6 tests -- there are 6 test /methods/, but 44 individual
assert statements within that file at time of writing.

To understand the code, we recommend you read through in the following order:
- species.py, the init and isAttackable functions
- playerState.py
- player.py, especially the feed function
- feedingAction.py
- tests.py
