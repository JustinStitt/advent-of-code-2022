import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

moves = lines[0]

WIDTH = 7
HEIGHT = 10_000
START_C = 2
START_R = HEIGHT - 4
cave = [[0] * WIDTH for _ in range(HEIGHT)]


def printCave():
    global shapes
    for r in range(9980, HEIGHT):
        for c in range(WIDTH):
            p = (r, c)
            inside = False
            for shape in shapes:
                if p in shape:
                    inside = True
            if inside:
                print("🟦", end="")
            else:
                print("⬛", end="")

        print(" ", r)


def createShape(sidx):
    global START_R, START_C
    sr, sc = START_R, START_C
    # make shape
    points = set()
    offs = []
    if sidx == 0:  # make hbar
        offs = [(0, 0), (0, 1), (0, 2), (0, 3)]
    elif sidx == 1:  # make cross
        offs = [(0, 1), (-1, 0), (-1, 1), (-1, 2), (-2, 1)]
    elif sidx == 2:  # make L
        offs = [(0, 0), (0, 1), (0, 2), (-1, 2), (-2, 2)]
    elif sidx == 3:  # make vbar
        offs = [(0, 0), (-1, 0), (-2, 0), (-3, 0)]
    elif sidx == 4:  # make square
        offs = [(0, 0), (0, 1), (-1, 0), (-1, 1)]

    for off in offs:
        points.add((sr + off[0], sc + off[1]))
    return points


shapes: set[frozenset] = set()

cmove = 0


def solve(sidx):
    global shapes, START_R, cmove
    points: set[tuple[int, int]] = createShape(sidx)
    # now move shape sideways
    # go sideways
    at_rest = False
    while 1:
        new_points = set()
        for point in points:
            # get current move
            dx = 1 if moves[cmove] == ">" else -1
            nx = point[1] + dx
            if nx < 0 or nx > WIDTH - 1:
                # print("hit wall")
                pass
            elif any([(point[0], nx) in shape for shape in shapes]):
                pass
                # print("hit shape sideways")
            else:
                new_points.add((point[0], nx))
        if len(new_points) == len(points):  # successfully moved entire shape
            points = new_points

        cmove = (cmove + 1) % len(moves)
        # now go down
        new_points = set()
        local_highest = HEIGHT + 1
        for p in points:
            new_points.add((p[0] + 1, p[1]))

        for np in new_points:
            r, c = np
            if r == HEIGHT:
                # print("came to rest at the floor")
                at_rest = True
                break
            elif any([np in shape for shape in shapes]):
                # print("came to rest atop a shape")
                at_rest = True
                break
        if at_rest:
            # get new highest point (technically the smallest)
            # smallest here
            # print(f"{new_points=}")
            local_highest = sorted(new_points, key=lambda x: x[0])[0][0]
            START_R = min(START_R, local_highest - 5)
            # print(f"{START_R=}")
            break
        points = new_points

    shapes.add(frozenset(points))
    # print(shapes)
    return True


if __name__ == "__main__":
    sidx = 0
    count = 2022
    while 1:
        if count == 0:
            break
        at_rest = solve(sidx)
        sidx = (sidx + 1) % 5
        count -= 1
    # printCave()
    print(HEIGHT - START_R - 4)
