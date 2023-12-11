## Day 1
- Do not move iterator after finding a whole word, because some words can have common parts. "oneight" contains both "one" and "eight".
## Day 2
- start iterating correctly (from 0 or from 1, depending on excercise)
- spell R G B correctly (your mistake was to spell R B G accidentally)
## Day 3
-  -index in python will start index from the end! This might be not what you want
- Check indexes for off-by-one error
- properly parse values from the edges of the map
## Day 5 and 6
- Instead of working on full ranges, maybe you can work only on range boundaries (intervals).
- When transforming range boundaries, the range can split into 1-2 additional ranges (intervals).
- The input to exercise might have some additional rules that make it easier: for example, can be alphabetically sorted or some parts can be exclusive so you dont have to worry about it. YOU DONT NEED A GENERIC SOLUTION
## Day 8
- If you have multiple cycles (and cycles within cycles) you probably want LCM .
- Observe if LCM works on test input and also check if cycle from A-Z is the same as Z-A. If yes, you can use LCM