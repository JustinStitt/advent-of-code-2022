import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

rows = len(lines)
cols = len(lines[0])

matrix = [[None for i in range(cols)] for ii in range(rows)]


class Node:
    def __init__(self, pos, marker):
        self.pos = pos
        self.marker = marker
        self.path = []


potential_starts = []
start = Node((0, 0), "a")
end = Node((0, 0), "z")

for (r, row) in enumerate(lines):
    for (c, col) in enumerate(row):
        matrix[r][c] = col
        if col == "a":
            potential_starts.append(Node((r, c), col))
        if col == "S":
            start.pos = (r, c)
        if col == "E":
            end.pos = (r, c)
# probably BFS? with rules


def bfs(pote):
    end, rows, cols, matrix
    Q = [pote]
    # start.path.append(start.pos)
    vis = set((pote.pos[0], pote.pos[1]))

    while len(Q):
        fn = Q.pop(0)
        if fn.pos == end.pos:
            print("FOUND GOAL")
            # print(fn.path)
            print(len(fn.path))
            return len(fn.path)
        # get neighbors of f (neighbors can only be height delta of 1)
        neighbor_offs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for off in neighbor_offs:
            rd, cd = off
            np = (fn.pos[0] + rd, fn.pos[1] + cd)
            if np[0] < 0 or np[0] > rows - 1:
                continue
            if np[1] < 0 or np[1] > cols - 1:
                continue
            neigh = matrix[np[0]][np[1]]
            if neigh == "E":
                neigh = "z"
            # height_delta = abs(ord(fn.marker) - ord(neigh))
            height_delta = ord(neigh) - ord(fn.marker)
            if height_delta > 1 or np in vis:
                # print(f"{fn.marker=}, {neigh=}")
                continue
            # otherwise good
            new_node = Node(np, neigh)
            new_node.path = fn.path[::]
            new_node.path.append(np)
            vis.add(np)
            Q.append(new_node)
    return 10e9


def printGrid():
    for row in matrix:
        for col in row:
            print(col, end="")
        print()


rezzis = []
for ps in potential_starts:
    rezzis.append(bfs(ps))

print(sorted(rezzis))
