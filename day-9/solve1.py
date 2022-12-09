import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

visited = set()  # (2, 3)


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y


knots = [Pos(0, 0) for _ in range(10)]
visited.add((0, 0))


def checkForTailMove(i):
    if i == 9:
        return  # last
    H, T = knots[i], knots[i + 1]
    # print(f"{H.x=}, {H.y=}, {T.x=}, {T.y=}, {i=}")
    og = (T.x, T.y)
    x_dist = H.x - T.x
    y_dist = H.y - T.y

    if abs(x_dist) <= 1 and abs(y_dist) <= 1:
        return  # no move
    # two in a single cardinal
    if x_dist == 2 and y_dist == 0:
        T.x += 1
    elif x_dist == -2 and y_dist == 0:
        T.x -= 1
    elif x_dist == 0 and y_dist == 2:
        T.y += 1
    elif x_dist == 0 and y_dist == -2:
        T.y -= 1

    if (T.x != og[0]) or (T.y != og[1]):  # changed!
        # go move dependent
        checkForTailMove(i + 1)
        if i == 8:
            visited.add((T.x, T.y))
        return
    # set Tail below if 2 above and to side if two side
    if x_dist == 2:
        T.x = H.x - 1
        T.y = H.y
    elif x_dist == -2:
        T.x = H.x + 1
        T.y = H.y
    elif y_dist == 2:
        T.x = H.x
        T.y = H.y - 1
    elif y_dist == -2:
        T.x = H.x
        T.y = H.y + 1

    checkForTailMove(i + 1)
    if i == 8:
        visited.add((T.x, T.y))  # add new position


for line in lines:
    H = knots[0]
    card, amnt = line.split()
    if card == "R":
        for _ in range(int(amnt)):
            H.x += 1
            checkForTailMove(0)
    elif card == "L":
        for _ in range(int(amnt)):
            H.x -= 1
            checkForTailMove(0)
    elif card == "U":
        for _ in range(int(amnt)):
            H.y -= 1
            checkForTailMove(0)
    elif card == "D":
        for _ in range(int(amnt)):
            H.y += 1
            checkForTailMove(0)


# print(visited)
print(len(visited))
"""
make a really big grid
and place head and tail in the middle
move head following rules
check if need to update tail
if two in cardinal, move to cardinal
if three manhattan, move diag always
"""
# not 2190
# rather 2372
