import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

visited = set()  # (2, 3)


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iadd__(self, off):
        xx, yy = off
        self.x += xx
        self.y += yy
        return self


knots = [Pos(0, 0) for _ in range(10)]
visited.add((0, 0))


# def checkForTailMove(i):
#     if i == 9:
#         return  # last
#     H, T = knots[i], knots[i + 1]
#     # print(f"{H.x=}, {H.y=}, {T.x=}, {T.y=}, {i=}")
#     og = (T.x, T.y)
#     x_dist = H.x - T.x
#     y_dist = H.y - T.y

#     if abs(x_dist) <= 1 and abs(y_dist) <= 1:
#         return  # no move
#     # two in a single cardinal
#     if x_dist == 2 and y_dist == 0:
#         T.x += 1
#     elif x_dist == -2 and y_dist == 0:
#         T.x -= 1
#     elif x_dist == 0 and y_dist == 2:
#         T.y += 1
#     elif x_dist == 0 and y_dist == -2:
#         T.y -= 1

#     if (T.x != og[0]) or (T.y != og[1]):  # changed!
#         # go move dependent
#         checkForTailMove(i + 1)
#         if i == 8:
#             visited.add((T.x, T.y))
#         return
#     # set Tail below if 2 above and to side if two side
#     if x_dist == 2:
#         T.x = H.x - 1
#         T.y = H.y
#     elif x_dist == -2:
#         T.x = H.x + 1
#         T.y = H.y
#     elif y_dist == 2:
#         T.x = H.x
#         T.y = H.y - 1
#     elif y_dist == -2:
#         T.x = H.x
#         T.y = H.y + 1

#     checkForTailMove(i + 1)
#     if i == 8:
#         visited.add((T.x, T.y))  # add new position

offs = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}
for line in lines:
    card, amnt = line.split()
    amnt = int(amnt)
    for _ in range(amnt):
        knots[0] += offs[card]

        for ii in range(len(knots) - 1):
            f, s = knots[ii : ii + 2]
            x_dist = abs(f.x - s.x)
            y_dist = abs(f.y - s.y)
            dist = x_dist + y_dist
            if dist <= 1:  # touching in cardinal dir
                continue
            dx = 1 if f.x > s.x else -1
            dy = 1 if f.y > s.y else -1
            if dist == 2 and x_dist != y_dist:  # two away in cardinal dir
                if x_dist:
                    s.x += dx
                elif y_dist:
                    s.y += dy
                if s is knots[-1]:
                    visited.add((s.x, s.y))
                continue

            if dist >= 2 and x_dist == y_dist:  # big diag away
                s.x += dx * (x_dist - 1)
                s.y += dy * (y_dist - 1)
                if s is knots[-1]:
                    visited.add((s.x, s.y))
                continue

            # two away in diag dir (knight move)
            big_is_x = abs(f.x - s.x) > abs(f.y - s.y)
            if big_is_x:
                s.y = f.y
                s.x = f.x - 1 if f.x > s.x else f.x + 1
            else:
                s.x = f.x
                s.y = f.y - 1 if f.y > s.y else f.y + 1

            if s is knots[-1]:
                visited.add((s.x, s.y))

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
