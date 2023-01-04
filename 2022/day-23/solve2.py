import sys
from collections import defaultdict
from copy import deepcopy

lines = [line.rstrip() for line in sys.stdin.readlines()]

# !! remember to consider if elf has no neighbors


class Elf:
    def __init__(self, r, c):
        self.r: int = r
        self.c: int = c
        self.current_check: int = 0

    def __repr__(self):
        return f"Elf({self.r=}, {self.c=}, {self.current_check=})"

    def checkSurroundings(self, current_check):  # self and elf! that's confusing
        global elves
        self.current_check = current_check
        (r, c) = (self.r, self.c)
        N = (r - 1, c) in elves
        NE = (r - 1, c + 1) in elves
        E = (r, c + 1) in elves
        SE = (r + 1, c + 1) in elves
        S = (r + 1, c) in elves
        SW = (r + 1, c - 1) in elves
        W = (r, c - 1) in elves
        NW = (r - 1, c - 1) in elves

        if all(not x for x in (N, NE, E, SE, S, SW, W, NW)):  # no elves around us
            # print(f"No Elves around us: {self.r=}, {self.c=}")
            return  # do nothing, not even update current_check!

        can_go = [-1] * 4  # 0: (r, c)
        if all(not x for x in (N, NE, NW)):  # no elves n, nw, ne
            can_go[0] = (r - 1, c)

        if all(not x for x in (S, SE, SW)):
            can_go[1] = (r + 1, c)

        if all(not x for x in (W, NW, SW)):
            can_go[2] = (r, c - 1)

        if all(not x for x in (E, NE, SE)):
            can_go[3] = (r, c + 1)

        proposed = None
        for i in range(4):
            check = (self.current_check + i) % 4
            if can_go[check] != -1:
                proposed = can_go[check]
                break  # stop at very first proposition

        return proposed


elves: dict[tuple[int, int], Elf] = {}  # (r, c): Elf()


def solve(round_no):
    global elves
    # proposed = defaultdict(lambda: list())
    proposed = dict()
    any_movement = False
    # get all the elves proposed moves
    for (pos, elf) in elves.items():
        proposed_pos = elf.checkSurroundings(round_no)
        # print(f"{proposed_pos=}")
        if proposed_pos:
            if proposed.get(proposed_pos, None) is not None:
                proposed[proposed_pos].append(elf)  # elf wants this position!
            else:
                proposed[proposed_pos] = [elf]

    # print(f"{proposed=}")
    # check proposed
    for (pos, interested_elves) in proposed.items():
        elf = interested_elves[0]
        # does another elf want this same position?
        if len(interested_elves) == 1:  # only if exactly one elf is interested
            del elves[(elf.r, elf.c)]
            any_movement = True
            elf.r, elf.c = pos
            elves[pos] = elf
    return any_movement


def drawState():
    global elves
    return
    # print(elves)
    for r in range(15):
        for c in range(15):
            sym = "#" if (r, c) in elves else "."
            print(sym, end="")
        print()


def main():
    global elves
    for (r, line) in enumerate(lines):
        for (c, char) in enumerate(line):
            if char != "#":  # not an elf
                continue
            pos = (r, c)
            elves[pos] = Elf(r, c)

    for round in range(2**11):
        # print(f"{round=}")
        rezzi = solve(round)
        if rezzi is False:
            print("STOPPED AT ROUND: ", round + 1)
            exit(0)
        drawState()
    # get bounding box
    min_r, min_c = (2**16, 2**16)
    max_r, max_c = -(2**16), -(2**16)
    for (pos, elf) in elves.items():
        min_r = min(min_r, pos[0])
        max_r = max(max_r, pos[0])
        min_c = min(min_c, pos[1])
        max_c = max(max_c, pos[1])

    # min_r -= 1
    # min_c -= 1
    max_r += 1
    max_c += 1
    total = 0
    for r in range(min_r, max_r):
        for c in range(min_c, max_c):
            total += 0 if (r, c) in elves else 1
    # drawState()
    print(f"{total=}")


if __name__ == "__main__":
    main()
