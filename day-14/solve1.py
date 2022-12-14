import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

ROWS = 10000
COLS = 10_000
AIR = 0
ROCK = 1
SAND = 2
cave = [[AIR for _ in range(ROWS)] for __ in range(COLS)]


def getAllPointsOnLine(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    points = []
    isSteep = abs(y2 - y1) > abs(x2 - x1)
    if isSteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
    dx = x2 - x1
    dy = y2 - y1
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
    y = y1
    for x in range(x1, x2 + 1):
        coord = (y, x) if isSteep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
    if swapped:
        points.reverse()
    return points


DROP_LOC = 500

num_sand_dropped = 0


def dropSand():
    global cave, AIR, SAND, ROCK
    # start at 0, 500
    cpos = [0, 500]

    while 1:
        # in the void?
        if cpos[0] >= 999:
            return 0  # tending towards abyss
        # # can we go down?
        # print(cpos)
        go_down = cave[cpos[0] + 1][cpos[1]] == AIR
        go_bl = cave[cpos[0] + 1][cpos[1] - 1] == AIR
        go_br = cave[cpos[0] + 1][cpos[1] + 1] == AIR
        if not go_down and not go_bl and not go_br:  # at rest
            cave[cpos[0]][cpos[1]] = SAND
            # did we lay to rest at the source?
            if cpos[0] == 0 and cpos[1] == 500:
                return 2
            return 1  # laid to rest
        if go_down:
            cpos[0] += 1
        elif go_bl:
            cpos[0] += 1
            cpos[1] -= 1
        elif go_br:
            cpos[0] += 1
            cpos[1] += 1


highest_y = -1
for line in lines:
    sp = line.split()[::2]
    for idx in range(len(sp) - 1):
        f, s = sp[idx : idx + 2]
        p1 = [int(x) for x in f.split(",")[::-1]]
        p2 = [int(x) for x in s.split(",")[::-1]]
        all_in_line = getAllPointsOnLine(p1, p2)
        for p in all_in_line:
            r, c = p
            highest_y = max(highest_y, r)
            cave[r][c] = 1

floor_r = highest_y + 2
# fill in the floor
for fc in range(0, 9998):
    cave[floor_r][fc] = ROCK
# drop sand!
while 1:
    res = dropSand()
    if res == 2:  # covered source
        break
    if res == False:  # tending towards the void
        break
    num_sand_dropped += 1

print(num_sand_dropped + 1)
