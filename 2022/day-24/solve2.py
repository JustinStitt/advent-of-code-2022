import sys
from queue import PriorityQueue
from dataclasses import dataclass, field

lines = [line.rstrip() for line in sys.stdin.readlines()]
ROWS = len(lines)
COLS = len(lines[0])
WALL = "#"
EMPTY = "."
BLIZZ = "^>v<"
start_pos = (0, 1)
end_pos = (ROWS - 1, COLS - 2)

current_pos = start_pos
grid = [[EMPTY for c in range(COLS)] for r in range(ROWS)]

blizzards = []


def parseInput():
    global grid, lines
    # print(grid)
    for r in range(ROWS):
        for c in range(COLS):
            if lines[r][c] != EMPTY:
                if lines[r][c] in BLIZZ:
                    blizzard = Blizzard(r, c, lines[r][c])
                    blizzards.append(blizzard)
                grid[r][c] = lines[r][c]


def printBoardState(minute, blizzard_states):
    global board, start_pos, end_pos, current_pos
    for (r, row) in enumerate(grid):
        for (c, col) in enumerate(row):
            sym = col
            if (r, c) == current_pos:
                sym = "C"
            elif (r, c) == start_pos:
                sym = "S"
            elif (r, c) == end_pos:
                sym = "E"
            elif (r, c) in blizzard_states[minute]:
                sym = "B"
            print(sym, end="")
        print()


class Blizzard:
    def __init__(self, r, c, d):
        self.pos = (r, c)
        self.dir = d

    def move(self):
        global grid
        dr = 1 if self.dir == "v" else -1 if self.dir == "^" else 0
        dc = 1 if self.dir == ">" else -1 if self.dir == "<" else 0
        # print(f"{dr=}, {dc=}")
        np = (self.pos[0] + dr, self.pos[1] + dc)
        if grid[np[0]][np[1]] == WALL:
            # print(f"hit wall")
            # loop backaround
            if dr == 1:
                self.pos = (1, self.pos[1])
            elif dr == -1:
                self.pos = (ROWS - 2, self.pos[1])
            elif dc == 1:
                self.pos = (self.pos[0], 1)
            elif dc == -1:
                self.pos = (self.pos[0], COLS - 2)
        else:
            self.pos = np


def generateBlizzardStates(n):
    global blizzards
    blizzard_states: list[set[int, int]] = [set() for _ in range(n)]
    directional_blizzard_states = [set() for _ in range(n)]
    # generate the first N minutes of blizzard states
    # for each blizzard simulate its movement over n minutes
    for (idx, blizzard) in enumerate(blizzards):
        for i in range(n):
            # log pos
            blizzard_states[i].add(blizzard.pos)  # state at minute `i` has this `pos`
            directional_blizzard_states[i].add(
                (blizzard.pos, blizzard.dir)
            )  # state at minute `i` has this `pos`
            # move the blizzard
            blizzard.move()

    return [frozenset(s) for s in blizzard_states], [
        frozenset(s) for s in directional_blizzard_states
    ]


def manhattanDistance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


@dataclass(order=True, unsafe_hash=True)
class State:
    pos: tuple[int, int] = field(compare=False, default=start_pos)
    minute: int = field(compare=False, default=0)
    wait_count: int = field(compare=False, default=0)
    priority: int = manhattanDistance(start_pos, end_pos)
    trip_status: int = field(
        compare=False, default=0
    )  # 0 going to end, going to start, going to end
    path: list[tuple[int, int]] = field(
        compare=False, default_factory=lambda: [start_pos]
    )


def getNeighbors(state: State, blizzard_states):
    global grid
    # go to all neighbors (can go N, E, S, W or wait)
    offs = [(1, 0), (0, 1), (0, -1), (-1, 0), (0, 0)]
    r, c = state.pos
    min = state.minute
    consider = []
    for (dr, dc) in offs:
        nr, nc = r + dr, c + dc

        if nr > ROWS - 1 or nr < 0 or nc > COLS - 1 or nc < 0 or grid[nr][nc] == WALL:
            continue  # don't run into walls or out of bounds (somehow)
        consider.append((r + dr, c + dc))

    # now get rid of states that have a blizzard in them
    available = []
    for possible in consider:
        if possible in blizzard_states[min + 1]:  # !! +1 or not?
            continue
        available.append(possible)
    return available


def printState(state: State, blizzard_states):
    global grid
    for r in range(ROWS):
        for c in range(COLS):
            sym = "⬜"
            if grid[r][c] == WALL:
                sym = "⬛"
            elif (r, c) == state.pos:
                sym = "🟦"
            if (r, c) in blizzard_states[state.minute]:
                sym = "🟥"
            if (r, c) in blizzard_states[state.minute] and (r, c) == state.pos:
                sym = "🟨"  # big WTF how this is possible lol !!
            print(sym, end="")
        print()


def bfs(blizzard_states, directional_blizzard_states):
    global grid, end_pos
    starting_state = State()
    best = 2**31
    # Q = [starting_state]
    Q = PriorityQueue()
    Q.put(starting_state)
    cache = {}
    debug_seen = set()

    MINUTE_THRESHOLD = 2048  # don't take longer than this! !! (change for pt2 ?)
    # MAX_WAITS_ALLOWED = 2**31  # don't wait more than 8 times

    while not Q.empty():
        curr = Q.get()

        if (
            curr.pos,
            curr.trip_status,
            directional_blizzard_states[curr.minute],
        ) in cache:
            print(f"cache hit")
            continue
        if curr.minute not in debug_seen:
            print(f"at minute: {curr.minute}")
            debug_seen.add(curr.minute)
        # probably prune here with if curr.minute > 100 ? or some X.
        if curr.minute > MINUTE_THRESHOLD:
            continue

        # cache[
        #     (curr.pos, curr.trip_status, directional_blizzard_states[curr.minute])
        # ] = 1

        if curr.trip_status == 1 and curr.pos == start_pos:  # back -> start
            curr.trip_status = 2  # now go to back to the end back

        if curr.pos == end_pos and curr.trip_status == 0:
            curr.trip_status = 1

        if curr.trip_status == 2 and curr.pos == end_pos:  # back -> start -> back
            print(f"Found Goal at minute: {curr.minute}")
            exit(1)
            # exit(1)
            # cache[(curr.pos, blizzard_states[curr.minute])] = curr.minute
            # print(f"{curr=}")
            best = min(best, curr.minute)
            continue

        for neighbor in getNeighbors(curr, blizzard_states):
            new_state = State(
                neighbor,
                curr.minute + 1,
                path=curr.path + [neighbor],
                trip_status=curr.trip_status,
            )
            # calculate priority
            prios = [2**64, 2**32, 2**0]
            new_priority = manhattanDistance(neighbor, end_pos)
            if curr.trip_status == 1:  # going to the start
                new_priority = manhattanDistance(neighbor, start_pos)
            if new_state.minute + new_priority >= best:
                continue  # don't add a state that can't beat our best!
            new_priority += prios[curr.trip_status]
            new_state.priority = new_priority
            Q.put(new_state)

        # if curr.wait_count < MAX_WAITS_ALLOWED:  # don't wait more than N times
        #     # waiting is also a possibility as long as no blizzard here in next minute
        #     blizzard_coming = curr.pos in blizzard_states[curr.minute + 1]
        #     if blizzard_coming:
        #         continue
        #     wait_state = State(curr.pos, curr.minute + 1, curr.wait_count + 1)
        #     Q.put(wait_state)

    return best


def main():
    parseInput()
    for row in grid:
        for col in row:
            print(col, end="")
        print()
    n = 2048
    (blizzard_states, directional_blizzard_states) = generateBlizzardStates(n)
    print(f"Done generating blizzard states")
    # for _ in range(18):
    #     print(f"Minute: {_}")
    #     printState(State(start_pos, _), blizzard_states)
    # t = 0
    # test_start = State((2, 3), t)
    # dstates = getNeighbors(test_start, blizzard_states)
    # printBoardState(t, blizzard_states)

    # print(dstates)
    rezzi = bfs(blizzard_states, directional_blizzard_states)
    print(f"{rezzi=}")


if __name__ == "__main__":
    main()


"""
idea:
solve every path, eliminate the ones that encounter a blizzard at that timestep

prune too long paths

"""
