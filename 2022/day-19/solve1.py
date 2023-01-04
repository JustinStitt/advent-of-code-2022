import sys
from copy import copy
import re
from dataclasses import dataclass
import functools

lines = [line.rstrip() for line in sys.stdin.readlines()]
TIMELIMIT = 24
blueprints = []


@dataclass(eq=True, frozen=True)
class Blueprint:
    id: int
    ore_ore_cost: int
    clay_ore_cost: int
    obsidian_ore_cost: int
    obsidian_clay_cost: int
    geode_ore_cost: int
    geode_obsidian_cost: int


def main():
    for line in lines:
        digits = re.findall(r"\d+", line)
        digits = [int(x) for x in digits]
        bp = Blueprint(*digits)
        blueprints.append(bp)


@dataclass(unsafe_hash=True)
class State:
    num_ore_robots: int = 1
    num_clay_robots: int = 0
    num_obsidian_robots: int = 0
    num_geode_robots: int = 0
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    time: int = TIMELIMIT


best_so_far = 0
cycle = 0


@functools.cache
def getNextStates(bp: Blueprint, state: State):
    global cycle, best_so_far
    cycle += 1
    best_so_far = max(best_so_far, state.geode + (state.num_geode_robots * state.time))
    if cycle % 200_000 == 0:
        print(f"{best_so_far=}")
    if state.time < 1:
        return state.geode
    if state.time < 5 and state.geode < 3:
        return state.geode
    if state.num_geode_robots < 2 and state.time < 2:
        return state.geode
    S = state
    all_states: list[State] = []
    ore_robots_constructable = S.ore // bp.ore_ore_cost
    clay_robots_constructable = S.ore // bp.clay_ore_cost
    obsidian_robots_constructable = min(
        S.ore // bp.obsidian_ore_cost, S.clay // bp.obsidian_clay_cost
    )
    geode_robots_constructable = min(
        S.ore // bp.geode_ore_cost, S.obsidian // bp.geode_obsidian_cost
    )
    state.time -= 1
    state.ore += state.num_ore_robots
    state.clay += state.num_clay_robots
    state.obsidian += state.num_obsidian_robots
    state.geode += state.num_geode_robots
    # print(state)
    # print(
    #     f"{ore_robots_constructable=}, {clay_robots_constructable=}, {obsidian_robots_constructable=}, {geode_robots_constructable=}"
    # )
    rezzis = [0] * 4
    if geode_robots_constructable > 0:
        new_state: State = copy(S)
        new_state.ore -= bp.geode_ore_cost
        new_state.obsidian -= bp.geode_obsidian_cost
        new_state.num_geode_robots += 1
        best_geode: list[State] = getNextStates(bp, new_state)
        rezzis[0] = best_geode
    if obsidian_robots_constructable > 0:
        new_state: State = copy(S)
        new_state.ore -= bp.obsidian_ore_cost
        new_state.clay -= bp.obsidian_clay_cost
        new_state.num_obsidian_robots += 1
        best_geode: list[State] = getNextStates(bp, new_state)
        rezzis[1] = best_geode
    if clay_robots_constructable > 0:
        new_state: State = copy(S)
        new_state.ore -= bp.clay_ore_cost
        new_state.num_clay_robots += 1
        best_geode: list[State] = getNextStates(bp, new_state)
        rezzis[2] = best_geode
    if ore_robots_constructable > 0:
        new_state: State = copy(S)
        new_state.ore -= bp.ore_ore_cost
        new_state.num_ore_robots += 1
        best_geode: list[State] = getNextStates(bp, new_state)
        rezzis[3] = best_geode

    neither = getNextStates(bp, state)

    return max(*rezzis, neither)


if __name__ == "__main__":
    main()
    # solve(blueprints[0])
    state = State()  # initial state (no resources, no robots)
    states = getNextStates(blueprints[1], state)
    best = max(states, key=lambda x: x.geode)
    print(f"{best=}")

# should we ever do nothing, even if robot purchasable?
