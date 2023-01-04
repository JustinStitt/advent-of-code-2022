import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

cubes = set()

for line in lines:
    x, y, z = line.split(",")
    cubes.add((int(x), int(y), int(z)))

# for every cube, check how many of its cubes are covered by another cube


# part 2... water sim lol, let's try it


def canFlow(point):
    global cubes
    # try to dfs out
    if point in cubes:
        return True
    stk = [point]
    visited = set()

    while len(stk):
        t = stk.pop()
        if t[0] > 18 or t[0] < -5:
            return True
        if t[1] > 18 or t[1] < -5:
            return True
        if t[2] > 18 or t[2] < -5:
            return True
        if t in visited:
            continue
        if t in cubes:
            continue  # hit another cube
        visited.add(t)
        x, y, z = t
        # go to each neighbor
        for dx in [-1, 1]:
            stk.append((x + dx, y, z))

        for dy in [-1, 1]:
            stk.append((x, y + dy, z))

        for dz in [-1, 1]:
            stk.append((x, y, z + dz))
    return False


inside_cubes = set()
for x in range(0, 20):
    for y in range(0, 20):
        for z in range(0, 20):
            p = (x, y, z)
            res = canFlow(p)
            if not res:
                # print("cant flow")
                # print(p)
                # add cube to cubes
                inside_cubes.add(p)
                # check how many faces it touches


def getSurfaceArea(cubes):
    total_area = len(cubes) * 6
    for cube in cubes:
        x, y, z = cube
        for delta in range(-1, 2):
            if delta == 0:
                continue
            dx = cube[0] + delta
            dy = cube[1] + delta
            dz = cube[2] + delta
            if (dx, y, z) in cubes:
                # print(f"{dx=}, {y=}, {z=}")
                total_area -= 1
            if (x, dy, z) in cubes:
                total_area -= 1
            if (x, y, dz) in cubes:
                total_area -= 1
    return total_area


if __name__ == "__main__":
    all_surface_area = getSurfaceArea(cubes)
    inside_surface_area = getSurfaceArea(inside_cubes)
    print(all_surface_area - inside_surface_area)
