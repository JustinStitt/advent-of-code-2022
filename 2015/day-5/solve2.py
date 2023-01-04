import sys
from collections import defaultdict
from aocdebug.debug import debug

DEBUG = True
debug = debug if DEBUG else lambda _: 0

lines = [line.rstrip() for line in sys.stdin.readlines()]

count = 0
for line in lines:
    A, B = False, False
    for i in range(len(line) - 1):
        pair = line[i : i + 2]
        if pair not in line[i + 2 :]:
            continue
        A = True

    for i in range(len(line) - 2):
        q, r, s = line[i : i + 3]
        if q == s:
            B = True
            break

    # debug(A, B, line)
    if A and B:
        count += 1

print(count)
