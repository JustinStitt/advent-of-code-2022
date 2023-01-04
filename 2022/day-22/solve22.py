import sys
import re
from dataclasses import dataclass
from copy import deepcopy

lines = [line.rstrip() for line in sys.stdin.readlines()]
OPEN = "."
WALL = "#"
NORTH, EAST, SOUTH, WEST = (0, 1, 2, 3)
N = 50  # 50 for big !!
faces = {"top": [], "front": [], "bottom": [], "left": [], "right": [], "back": []}
faces["top"] = [line.lstrip() for line in lines[0:N]]
faces["front"] = [line[N * 2 :] for line in lines[N : N * 2]]
faces["bottom"] = [line[N * 2 : N * 3] for line in lines[N * 2 : N * 3]]
faces["left"] = [line[N : N * 2] for line in lines[N : N * 2]]
faces["right"] = [line[N * 3 :] for line in lines[N * 2 : N * 3]]
faces["back"] = [line[:N] for line in lines[N : N * 2]]
faces_debug = deepcopy(faces)
debug_count = 0
debug_hex = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 5000

facetoface = {
    "front": {NORTH: "top", EAST: "right", SOUTH: "bottom", WEST: "left"},
    "top": {NORTH: "back", EAST: "right", SOUTH: "front", WEST: "left"},
    "bottom": {NORTH: "front", EAST: "right", SOUTH: "back", WEST: "left"},
    "left": {NORTH: "top", EAST: "front", SOUTH: "bottom", WEST: "back"},
    "right": {NORTH: "front", EAST: "top", SOUTH: "back", WEST: "bottom"},
    "back": {NORTH: "top", EAST: "left", SOUTH: "bottom", WEST: "right"},
}

# unhinged
facetodir = {
    # (from, to)
    ("front", "right"): SOUTH,  # SOUTH
    ("right", "top"): WEST,  #
    ("right", "back"): EAST,  #
    ("right", "front"): WEST,  #
    ("top", "right"): WEST,  #
    ("top", "back"): SOUTH,
    ("top", "left"): SOUTH,
    ("back", "top"): SOUTH,
    ("back", "right"): NORTH,
    ("back", "bottom"): NORTH,
    ("left", "top"): EAST,  #
    ("left", "bottom"): EAST,  #
    ("bottom", "left"): NORTH,
    ("bottom", "back"): NORTH,
}
# 10R5L5R10L4R5L5
raw_commands = lines[-1]
amounts = re.findall(r"\d+", raw_commands)
turns = re.findall(r"[RL]", raw_commands)

# print(amounts)
# print(turns)


def drawDebug(agent):
    global debug_count, debug_hex, debug_curr
    sym = "^"
    if agent.direction == EAST:
        sym = ">"
    elif agent.direction == SOUTH:
        sym = "v"
    elif agent.direction == WEST:
        sym = "<"
    debug_curr = faces_debug[agent.current_face][agent.r]
    faces_debug[agent.current_face][agent.r] = "".join(
        [
            debug_curr[i] if i != agent.c else debug_hex[debug_count]
            for i in range(len(debug_curr))
        ]
    )
    debug_count += 1


class Agent:
    def __init__(self):
        self.direction: int = EAST
        self.r: int = 0
        self.c: int = 0
        self.current_face = "top"

    def getNewFace(self) -> tuple[int, int]:
        global facetoface
        # face to face mappings

        cf = self.current_face
        return facetoface[cf][self.direction]

    def move(self, amount: int) -> None:
        global faces, debug_count
        if amount == 0:
            return  # nothing to do!

        dr = -1 if self.direction == NORTH else (1 if self.direction == SOUTH else 0)
        dc = -1 if self.direction == WEST else (1 if self.direction == EAST else 0)
        nr = self.r + dr
        nc = self.c + dc
        if nr > N - 1 or nc > N - 1 or nr < 0 or nc < 0:
            # print("before: ", nr, nc)
            # handle row based face transfer
            new_face = self.getNewFace()
            hinged = facetodir.get((self.current_face, new_face), None) is not None
            # print(f"{hinged=}")
            new_direction = facetodir.get((self.current_face, new_face), self.direction)
            # print(f"{new_direction=}")
            # print(f"{self.current_face=}, {new_face=}")
            # maintain column, but change row
            if new_direction == NORTH:
                if hinged and self.direction == WEST:
                    nc = N - 1 - self.r
                if hinged and self.direction == SOUTH:
                    nc = N - 1 - self.c
                if hinged and self.direction == EAST:
                    nc = self.c
                nr = N - 1
            elif new_direction == SOUTH:
                if hinged and self.direction == EAST:
                    nc = N - 1 - self.r
                if hinged and self.direction == NORTH:
                    nc = N - 1 - self.c
                if hinged and self.direction == WEST:
                    nc = self.r
                nr = 0
            # handle col based face transfer
            elif new_direction == EAST:
                if hinged and self.direction == SOUTH:
                    nr = N - 1 - self.c
                if hinged and self.direction == NORTH:
                    nr = self.c
                nc = 0
            elif new_direction == WEST:
                if hinged and self.direction == EAST:
                    nr = N - 1 - self.r
                if hinged and self.direction == NORTH:
                    nr = N - 1 - self.c
                nc = N - 1
            # new_spot = self.board[nr][nc]
            print(nr, nc)
            print(faces[self.current_face])
            print(f"from: {self.current_face} to: {new_face}")
            print(f"from: {self.direction} to: {new_direction}")
            print(f"{new_face=}")
            print(f"{faces[new_face]=}")
            print(f"{faces['front']=}")

            new_spot = faces[new_face][nr][nc]
            # print(f"{new_spot=}")
            if new_spot == WALL:
                return  # can't make this move!
            self.direction = new_direction
            self.current_face = new_face
            self.r = nr
            self.c = nc
            drawDebug(self)
            return self.move(amount - 1)

        # spot = self.board[nr][nc]
        spot = faces[self.current_face][nr][nc]
        if spot == WALL:  # run into wall!
            # print(f"HIT WALL!")
            # print(f"{self.r=}, {self.c=}, {self.direction=}")
            return  # stop moving in this direction, it's useless
        elif spot == OPEN:  # empty spot! move there!
            self.r = nr
            self.c = nc
            drawDebug(self)
            return self.move(amount - 1)

    def turn(self, direction: str) -> None:
        if direction == "R":
            self.direction = (self.direction + 1) % 4
        elif direction == "L":
            self.direction = self.direction - 1
            if self.direction < 0:
                self.direction = WEST
        else:
            print(f"Illegal Direction Passe: {direction=}")
            exit(1)  # bad


agent = Agent()


def printState(agent: Agent):
    print(f"{agent.current_face=}, {agent.r=}, {agent.c=}, {agent.direction=}")
    for (k, v) in faces.items():
        print(f"Face: {k}")
        for (i, item) in enumerate(v):
            for (j, c) in enumerate(item):
                to_print = c
                if k == agent.current_face and (i, j) == (agent.r, agent.c):
                    to_print = "X"
                print(to_print, end="")
            print()

    # actual_r = agent.r + 1
    # actual_c = agent.c + 1
    ad = 0
    d = agent.direction
    if d == NORTH:
        ad = 3
    elif d == EAST:
        ad = 0
    elif d == WEST:
        ad = 2
    else:
        ad = 1
    print("=" * 50)
    # result = 1000 * actual_r + 4 * actual_c + ad
    # print(f"{result=}")


# agent.move(2)
# agent.turn("R")
# agent.move(1)
# agent.turn("L")
# agent.move(2)
commands = []
for i in range(len(turns)):
    commands.append(amounts[i])
    commands.append(turns[i])
commands.append(amounts[-1])

for command in commands:
    if command in ("L", "R"):
        agent.turn(command)
        print("turn: ", command)
    else:
        agent.move(int(command))
        print("move: ", command)
    # printState(agent)
print("\n" * 10)
for (face, grid) in faces_debug.items():
    print(f"Face: {face}")
    for line in grid:
        for c in line:
            print(c, end="")
        print()

print(f"{agent.r=}, {agent.c=}, {agent.direction=}, {agent.current_face=}")
print(faces_debug)
