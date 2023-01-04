import sys
from copy import deepcopy, copy
import re
from dataclasses import dataclass
import functools
from queue import Queue

kTIMELIMIT = 24


@dataclass(eq=True, frozen=True)  # make hashable
class Blueprint:
    id: int
    ore_cost: tuple[int]
    clay_cost: tuple[int]
    obsidian_cost: tuple[int]
    geode_cost: tuple[int]


class State:
    def __init__(self):
        self.time: int = 24
        self.resource: list[int] = [0, 0, 0, 0]
        self.robots: list[int] = [1, 0, 0, 0]  # start with 1 ore robot

    def __repr__(self):
        return f"State({self.time=}, {self.resource=}, {self.robots=})"


def canPurchase(resources, cost):
    for (r, c) in zip(resources, cost):
        if r < c:
            return False
    return True


seen = [False] * 27


def bfs(bp: Blueprint):
    starting_state = State()  # starting state
    robot_costs = [bp.ore_cost, bp.clay_cost, bp.obsidian_cost, bp.geode_cost]
    Q = Queue()
    Q.put(starting_state)
    max_geodes = 0

    while not Q.empty():
        S = Q.get()
        if S.time == 0:
            max_geodes = max(max_geodes, S.resource[-1])
            continue
        if (
            max_geodes - S.resource[-1]
            >= (S.time * (2 * S.robots[-1] + S.time - 1)) // 2
        ):
            continue
        if not seen[S.time]:
            print(f"At Time: {S.time}")
            seen[S.time] = True
        S.time -= 1
        # print(f"{S=}")
        # check geode count against max

        for (idx, robot_cost) in enumerate(robot_costs):
            if canPurchase(S.resource, robot_cost) is False:
                continue
            # prune if we have too many of a single type already
            # buy the robot
            new_state = deepcopy(S)
            new_state.robots[idx] += 1
            new_state.resource = [
                new_state.resource[x] - robot_cost[x] for x in range(4)
            ]
            Q.put(new_state)
        # collect resources
        for (idx, robot_count) in enumerate(S.robots):
            # farm resources for parallel array robot
            # print(f"{idx=}, {robot_count=}, {S=}")
            S.resource[idx] += robot_count
        Q.put(deepcopy(S))  # relies on time limit to stop infinite loop

    return max_geodes


def main():
    global seen
    lines = [line.rstrip() for line in sys.stdin.readlines()]
    results = []
    for line in lines:
        d = [int(x) for x in re.findall(r"\d+", line)]
        bp = Blueprint(
            d[0],
            (d[1], 0, 0, 0),
            (d[2], 0, 0, 0),
            (d[3], d[4], 0, 0),
            (d[5], 0, d[6], 0),
        )
        result = bfs(bp)
        print(f"{result=}")
        results.append(result)
        seen = [False for _ in seen]
    print(f"{results=}")


if __name__ == "__main__":
    main()
