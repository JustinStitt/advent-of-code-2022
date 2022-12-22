import sys
import re
from dataclasses import dataclass

lines = [line.rstrip() for line in sys.stdin.readlines()]
EMPTY = "⬛"
OPEN = "⬜"
WALL = "🟥"
rendering = {" ": EMPTY, ".": OPEN, "#": WALL}
longest = max([len(line) for line in lines[:-2]])
padding = 32
grid = ["".join([rendering[y] for y in x]) for x in lines[:-2]]
for (idx, row) in enumerate(grid):
    row = EMPTY * padding + row + EMPTY * (longest - len(row) + padding)
    grid[idx] = row

for _ in range(padding):
    padding_row = EMPTY * padding * 2 + EMPTY * longest
    grid.insert(0, padding_row)
    grid.append(padding_row)

# 10R5L5R10L4R5L5
raw_commands = lines[-1]
amounts = re.findall(r"\d+", raw_commands)
turns = re.findall(r"[RL]", raw_commands)

# print(amounts)
# print(turns)

NORTH, EAST, SOUTH, WEST = (0, 1, 2, 3)


class Agent:
    def __init__(self, board):
        self.direction: int = EAST
        if not board:
            print(f"Bad Board: {board=}")
            exit(1)
        self.board: list[str] = board
        self.start = (padding, grid[padding].index(OPEN))  # !!
        print(self.start)
        self.r: int = self.start[0]
        self.c: int = self.start[1]

    def findFirstOpen(self) -> tuple[int, int]:
        if self.direction == EAST:
            # find first starting from left of current row
            current_row = self.board[self.r]
            for (c, cell) in enumerate(current_row):
                if cell == OPEN or cell == WALL:
                    return (self.r, c)
        elif self.direction == WEST:
            # find first starting from left of current row
            current_row = self.board[self.r]
            for i in range(len(current_row) - 1, -1, -1):
                cell = current_row[i]
                if cell == OPEN or cell == WALL:
                    return (self.r, i)
        elif self.direction == SOUTH:
            # find first starting from left of current row
            current_col = [self.board[r][self.c] for r in range(len(self.board))]
            for (r, cell) in enumerate(current_col):
                if cell == OPEN or cell == WALL:
                    return (r, self.c)
        elif self.direction == NORTH:
            # find first starting from left of current row
            current_col = [self.board[r][self.c] for r in range(len(self.board))]
            for i in range(len(current_col) - 1, -1, -1):
                cell = self.board[i][self.c]
                if cell == OPEN or cell == WALL:
                    return (i, self.c)

    def move(self, amount: int) -> None:
        if amount == 0:
            return  # nothing to do!
        dr = -1 if self.direction == NORTH else (1 if self.direction == SOUTH else 0)
        dc = -1 if self.direction == WEST else (1 if self.direction == EAST else 0)
        nr = self.r + dr
        nc = self.c + dc

        spot = self.board[nr][nc]
        if spot == EMPTY:  # wrap around
            first_open = self.findFirstOpen()
            if self.board[first_open[0]][first_open[1]] == WALL:
                return  # hit wall on wraparound
            self.r, self.c = first_open
            return self.move(amount - 1)
        elif spot == WALL:  # run into wall!
            print(f"HIT WALL!")
            print(f"{self.r=}, {self.c=}, {self.direction=}")
            return  # stop moving in this direction, it's useless
        elif spot == OPEN:  # empty spot! move there!
            self.r = nr
            self.c = nc
            self.move(amount - 1)

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


agent = Agent(grid)


def printState(agent: Agent, board: list[str]):
    for r in range(len(board)):
        for c in range(len(board[r])):
            to_print = board[r][c] if (agent.r, agent.c) != (r, c) else "🟦"
            print(to_print, end="")
        print()
    actual_r = agent.r - padding + 1
    actual_c = agent.c - padding + 1
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
    print(f"{actual_r=}, {actual_c=}")
    result = 1000 * actual_r + 4 * actual_c + ad
    print(f"{result=}")


# agent.turn("L")
# agent.move(3)
# printState(agent, agent.board)
commands = []
for i in range(len(turns)):
    commands.append(amounts[i])
    commands.append(turns[i])
commands.append(amounts[-1])
print(commands)

for command in commands:
    if command in ("L", "R"):
        agent.turn(command)
    else:
        agent.move(int(command))
printState(agent, agent.board)
