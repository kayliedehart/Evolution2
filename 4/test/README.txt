README - Assignment 4 Task 2 (Tests)

*-in.json - what the server should send to a 6 Nimmt! client
*-out.json - what the corresponding client should return

These test files represent sets of interactions between a 6 Nimmt! client and 
server. Set 1 tests a full set of rounds for correctness, as well as the timing 
for a second start-round message; set 2 tests a game without a start-round 
function; set 3 tests for choose before take-turn; set 4 tests for handling 
of nonsense messages; set 5 tests the timing for choose even when a turn has
been taken. All sets assume that, as specified in the assignment, a player 
should exit as soon as it gets malformed messages of any kind, though it 
will only send false if timing is bad, NOT if an unrecognizable message arrives.
