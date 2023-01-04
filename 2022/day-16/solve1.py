import sys, os
from collections import defaultdict

lines = [line.rstrip() for line in sys.stdin.readlines()]
# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB

# Edges
G = defaultdict(lambda: set())  # G['AA'].add('DD')
# Flows
F = defaultdict(lambda: int())  # G['AA'] = 0


for line in lines:
    line = line.split()
    fro, flowrate, neighbors = line[1], line[4], line[9:]
    flowrate = int(flowrate[flowrate.index("=") + 1 : -1])
    neighbors = [x[:2] for x in neighbors]
    # print(f"{fro=}, {flowrate=}, {neighbors=}")
    F[fro] = flowrate
    for neighbor in neighbors:
        G[fro].add(neighbor)

# solve
time_left = 30
total_flow = 0
num_non_zero = [1 for (k, v) in F.items() if v != 0]
# if str, then moved
# if int, then opened
def dfs(valve, mins, opened):
    # print(f"{valve=}, {idx=}")
    # out of time?
    if len(mins) > 30:
        # print("OUT OF TIME!")
        # print(f"{mins=}")
        return
    if len(opened) == num_non_zero:
        # print("USED ALL NON-ZERO VALVES!")
        return
    # either open valve we're currently at
    # or move onto a neighbor of the valve we're currently at
    for neighbor in G[valve]:
        if neighbor not in opened and F[neighbor] > 0:
            cmins = mins[::]  # copy of mins
            cmins.append(F[neighbor])
            opened.add(neighbor)
            # print(f"USING: {neighbor=}")
            dfs(neighbor, cmins, opened.copy())  # open our current valve

        dfs(neighbor, mins[::] + [valve], opened.copy())  # don't open valve
        # open valve
    # try both! log in copy of mins list


def solve():
    start = "AA"
    dfs(valve=start, mins=[], opened=set())


if __name__ == "__main__":
    solve()

"""
brute force:
start at 'AA'
consider two options at each... Open Valve, or move to other valve
keep running sum/max of flow rate... try all options! LOW N

some heuristics:
don't open 0 flow rate valves!

"""
