import sys
import re
from pipe import traverse
from collections import defaultdict
from aocdebug.debug import debug

DEBUG = True
debug = debug if DEBUG else lambda *_: 0

lines = [line.rstrip() for line in sys.stdin.readlines()]

OFF = 0
ON = 1

grid = [[OFF for __ in range(1000)] for _ in range(1000)]

intervals = []  # (r1, c1, r2, c2)

for line in lines:
    # extract two intervals
    fm, sm = re.findall(r"\d+,\d+", line)
    fm = [int(x) for x in fm.split(",")]
    sm = [int(x) for x in sm.split(",")]
    # debug(fm, sm)

    # determine type of interval (turn on, turn off, toggle)
    turn_on = "on" in line
    turn_off = "off" in line
    turn_toggle = "toggle" in line

    for r in range(fm[0], sm[0] + 1):
        for c in range(fm[1], sm[1] + 1):
            if turn_on:
                grid[r][c] += 1
            elif turn_off:
                grid[r][c] = max(grid[r][c] - 1, 0)
            elif turn_toggle:
                grid[r][c] += 2

# count number of lights turned on
answer = sum(grid | traverse)
print(answer)
