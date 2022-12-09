import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

mat = [[0] * len(lines) for x in range(len(lines))]
n = len(lines)

_r = 0
for (j, line) in enumerate(lines):
    for (i, c) in enumerate(line):
        mat[j][i] = int(c)

best = 0
for r in range(n):
    for c in range(n):
        score = 0
        us = mat[r][c]
        left, right, up, down = 0, 0, 0, 0
        allleft = mat[r][:c]
        allright = mat[r][c + 1 :]
        allup = [mat[_r][c] for _r in range(r - 1, -1, -1)]
        alldown = [mat[_r][c] for _r in range(r + 1, n)]

        for tree in allleft[::-1]:
            if tree >= us:
                left += 1
                break
            left += 1

        for tree in allright:
            if tree >= us:
                right += 1
                break
            right += 1

        for tree in allup:
            if tree >= us:
                up += 1
                break
            up += 1

        for tree in alldown:
            if tree >= us:
                down += 1
                break
            down += 1
        score = up * down * left * right
        best = max(score, best)

print(best)
