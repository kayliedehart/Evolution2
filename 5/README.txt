README - Assignment 5

xattack - a test harness that takes json input and runs isAttackable
player-interface.txt - a specification for Evolution player wrt dealer
test_xattack.py - a set of unit tests for xattack

To run xattack, type:
	./xattack < some-input.json [> some-output.json]
Without an output redirect, it will print to the terminal instead. You can also
run it by invoking it with any python 2.7 interpreter, though you may need to
remove the opening shebang (on Windows, it was run by removing it and typing 
	py xattack < some-input.json > some-output.json
).

test_xattack.py should be runnable by invoking ./test_xattack.py. However, you 
may need to change the PYTHON2_PATH variable to your own python 2.7 binary -- 
py.exe invokes python 2.7 on my Windows machine, but may not work or exist on 
others. 


To understand the code, you'll likely want to read attack/species.py first; this
is merely a proxy for the isAttackable() function in that file. The tests for 
xattack were not meant to test the functionality of isAttackable(), just that 
xattack was outputting the expected kind of values. 

To understand player-interface.txt, read the writeup at the beginning of the 
file, then work through the list of stubs and their comments.
