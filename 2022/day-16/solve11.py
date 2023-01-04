import sys, os
from collections import defaultdict
import itertools

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

# solve
total_flow = 0
num_non_zero = [1 for (k, v) in F.items() if v != 0]


def getCostMatrix(valve, seen):
    global G, F
    # from a valve, what is the min to flowrate ratio?
    # cost ratios val / min
    path_matrix = defaultdict(lambda: list())  # cm['BB'] = 6.5
    best_ratio = [valve, 0, [valve]]
    # bfs
    Q = [[valve, 1, [valve]]]
    vis = set()

    while len(Q):
        curr, minute, path = Q.pop(0)
        vis.add(curr)
        val = F[curr]
        ratio = val / minute
        path_matrix[curr] = path
        if (
            ratio > best_ratio[1] and valve != curr and curr not in seen
        ):  # dont consider self??
            best_ratio = [curr, ratio, path]
        # print(curr, ": ", G[curr])
        for neighbor in G[curr]:
            if neighbor in vis:
                continue
            Q.append([neighbor, minute + 1, path[::] + [neighbor]])
    return path_matrix


# print(f"{G=}, {F=}")

non_zero = [k for (k, v) in F.items() if v != 0]


def generateOrders():
    global F, G, start, non_zero
    print("generating orders...")
    non_zero_sorted = sorted(non_zero, key=lambda x: F[x], reverse=True)
    # permutations of all non-zero valves
    perms = itertools.permutations(non_zero_sorted)
    print("done generating orders!")
    return perms


def distanceBetween(u, v):
    global G, F

    Q = [[u, 0]]
    vis = set()

    while len(Q):
        curr, dist = Q.pop(0)
        if curr == v:  # we found v
            return dist
        for neighbor in G[curr]:
            if neighbor in vis:
                continue
            vis.add(neighbor)
            Q.append([neighbor, dist + 1])
    return -1  # not found


cost_matrix = defaultdict(lambda: float())


def computeDistancesBetween():
    global G, F, non_zero, cost_matrix
    non_zero_copy = non_zero[::] + [start]
    n = len(non_zero_copy)
    distances = defaultdict(lambda: int(-1))
    for i in range(n - 1):
        for j in range(i + 1, n):
            d = distanceBetween(non_zero_copy[i], non_zero_copy[j])
            s = non_zero_copy[i]
            e = non_zero_copy[j]
            distances[(s, e)] = d
            distances[(e, s)] = d
            cost_matrix[(s, e)] = F[e] / (d + 1)
            cost_matrix[(e, s)] = F[s] / (d + 1)
    return distances


# 2232 good save
def solve(order):
    global start, all_distances
    _start = start
    order = list(order) + [start]
    order = iter(order)
    time_left = 30
    total = 0
    curr = start
    seen = set([curr])
    # order = iter(["DD", "BB", "JJ", "HH", "EE", "CC", "AA"])
    # order = iter(["DD", "JJ", "BB", "HH", "EE", "CC", "AA"])
    select = next(order)
    while 1:
        if select == start:
            break
        cost = all_distances[(curr, select)] + 1
        # print(f"From: {curr} to {select} costs: {cost}")
        curr = select
        minutes_taken = cost
        time_left -= minutes_taken
        if time_left < 1:
            break
        total += time_left * F[select]

        select = next(order)
        # print(f"Opening valve: {curr} going to {select} {time_left=} {total=}")
    return total


all_distances = computeDistancesBetween()
if __name__ == "__main__":
    # print(all_distances)
    # print(cost_matrix[("AA", "JJ")])
    orders = generateOrders()
    rezzi = 0
    at = 0
    count = 100000000
    for order in orders:
        at += 1
        if at % 1000000 == 0:
            print(f"{at/count * 100}%")
        if at > count:
            break
        rezzi = max(rezzi, solve(order))
    print(f"{rezzi=}")

"""
brute force:
start at 'AA'
consider two options at each... Open Valve, or move to other valve
keep running sum/max of flow rate... try all options! LOW N

some heuristics:
don't open 0 flow rate valves!

"""
# potential rezzi=259, rezzi=973 (too low)
