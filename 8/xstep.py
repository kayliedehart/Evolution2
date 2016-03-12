#!/usr/bin/env python2.7
# A test harness for the Dealer's feed1 method

import sys
import json
from dealer.dealer import *
from feeding.jsonParsing import *

try:
    testInput = json.load(sys.stdin)
    if len(testInput) == 3:
    	curDealer = dealerFromJson(testInput)
        curDealer.feed1()
        result = [curDealer.players, curDealer.wateringHole, curDealer.deck]
        print json.dumps(result)

except Exception as e:
    quit()
