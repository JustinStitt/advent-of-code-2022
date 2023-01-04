import sys, os
from collections import defaultdict
import functools

lines = [line.rstrip() for line in sys.stdin.readlines()]
# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB

# Edges
G = defaultdict(lambda: set())  # G['AA'].add('DD')
# Flows
F = defaultdict(lambda: int())  # G['AA'] = 0

start = "AA"

for (idx, line) in enumerate(lines):
    line = line.split()
    fro, flowrate, neighbors = line[1], line[4], line[9:]
    flowrate = int(flowrate[flowrate.index("=") + 1 : -1])
    neighbors = [x[:2] for x in neighbors]
    # print(f"{fro=}, {flowrate=}, {neighbors=}")
    F[fro] = flowrate
    for neighbor in neighbors:
        G[fro].add(neighbor)


@functools.cache
def dfs(current, minutes, opened, elephants_turn=False):
    if minutes < 1 and elephants_turn is False:
        return dfs(start, 26, opened, True)  # restart with elephant's timer
    if minutes < 1 and elephants_turn is True:
        return 0
    best = 0
    flow = F[current]

    new_opened = opened + "-"
    if current not in opened and flow > 0:
        new_opened += current

    for neighbor in G[current]:
        best = max(best, dfs(neighbor, minutes - 1, opened, elephants_turn))
        if new_opened[-1] != "-":  # we opened something
            adjusted_flow = flow * (minutes - 1)
            best = max(
                best,
                adjusted_flow + dfs(neighbor, minutes - 2, new_opened, elephants_turn),
            )
    return best


if __name__ == "__main__":
    rezzi = dfs(start, 26, "")
    print(rezzi)
