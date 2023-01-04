import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

mat = [[0] * len(lines) for x in range(len(lines))]
n = len(lines)

_r = 0
for (j, line) in enumerate(lines):
    for (i, c) in enumerate(line):
        mat[j][i] = int(c)

total = 0
for r in range(n):
    for c in range(n):
        us = mat[r][c]
        if r == 0 or c == 0 or r == n - 1 or c == n - 1:  # on the edge
            total += 1
            continue
        # shorter than to left?
        left = mat[r][:c]
        right = mat[r][c + 1 :]
        up = [mat[_r][c] for _r in range(r - 1, -1, -1)]
        # print(f"{r=}, {c=}, {up=}")
        down = [mat[_r][c] for _r in range(r + 1, n)]
        tallest_to_left = max(left)
        if us > tallest_to_left:
            total += 1
            continue
        if us > max(right):
            total += 1
            continue
        print(up)
        if us > max(up):
            total += 1
            continue
        if us > max(down):
            total += 1
            continue
print(total)
