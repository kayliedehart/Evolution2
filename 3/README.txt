README - patches for task 1, protocol for task 2
 
starting-config.patch - links take5/Player.py to 2/take5/
test-config.patch - links take5/Player.py to 2/take5/ for tests
210-cards.patch - up the number of cards from 140 to 210
deal-nine.patch - deal 9 cards per player instead of 10
increasing-order.patch - players play their lowest card first
min-bullpoints.patch - up the minimum bullpoints from 2 to 3
take-6.patch - players pick up stacks of 6 instead of 5
player-protocol.txt - specifications for a distributed game


To apply any patch, run "patch -p1 < 3/$patchname" from the directory above this one. 
starting-config.patch MUST be applied for the program to run (see 2/take5/README.txt).
After that, patches can be applied in any order/configuration.


player-protocol.txt can be read in any order, but we recommend you start with the 
ASCII diagram at the top and work your way down through our notes and data structures.

starting-config required a two-line change, as we needed to import sys before
using sys to append this directory to the path.

test-config require the same two-line change as starting-config, but this takes
place in the test files in order for tests to run.

increasing-order required a two-line change because the index of the card being
picked up is not parameterized and must be referenced both when picking it up
and removing it from the player's held cards.

deal-nine required three line changes in the reference to the function name 
(dealTenToEach -> dealToEach) and another four in direct references to the number
of cards being 10 instead of 9, as this number was not parameterized.




