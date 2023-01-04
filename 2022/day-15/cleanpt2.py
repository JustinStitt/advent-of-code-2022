import re
import sys
from itertools import pairwise
from collections import defaultdict

lines = [line.rstrip() for line in sys.stdin.readlines()]

sensors = []
beacons = []
for line in lines:
    matches = re.findall(r"-?\d+", line)
    sx, sy, bx, by = [int(x) for x in matches]
    sensors.append((sx, sy))
    beacons.append((bx, by))

CUTOFF = 4_000_000
ranges = defaultdict(lambda: list())

for (sensor, beacon) in zip(sensors, beacons):
    sx, sy = sensor
    bx, by = beacon
    dist = abs(sx - bx) + abs(sy - by)  # manhattan distance
    for _y in range(sy - dist, sy + dist + 1):
        leftover = dist - abs(_y - sy)
        # xrange = [max(0, sx - leftover), min(sx + leftover, CUTOFF)]
        xrange = [sx - leftover, sx + leftover]
        ranges[_y].append(xrange)


def combineRanges(ranges):
    ascending = sorted(ranges, key=lambda x: x[0])
    # print(ascending)
    merged = []
    for curr in ascending:
        if curr[0] < 0:
            curr[0] = 0
        if curr[1] > CUTOFF:
            curr[1] = CUTOFF
        if not merged:
            merged.append(curr)
            continue
        prev = merged[-1]
        if prev[1] + 1 >= curr[0]:
            prev[1] = max(prev[1], curr[1])
            continue
        merged.append(curr)
    return merged


for (ylevel, _ranges) in ranges.items():
    if ylevel not in range(0, CUTOFF + 1):
        continue
    combined = combineRanges(_ranges)
    if len(combined) == 2:
        x = combined[0][1] + 1
        print(f"{x=}, y={ylevel}")
        print(f"Answer: {x*CUTOFF + ylevel}")
        break
